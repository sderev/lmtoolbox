import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from functools import wraps
from pathlib import Path

import click
import requests
import validators
import yaml
from lmterminal.cli import validate_model_name, validate_temperature
from lmterminal.lib import DEFAULT_MODEL, prepare_and_generate_response
from lmterminal.templates import TEMPLATES_DIR, get_template_content
from strip_tags.lib import strip_tags

from . import video_summarization


def install_templates():
    """
    Installs the templates in ~/.config/lmt/templates.
    """
    dest_path = Path.home() / ".config/lmt/templates"
    dest_path.mkdir(parents=True, exist_ok=True)

    config_file = Path.home() / ".config/lmt/config.json"
    config_file.touch(exist_ok=True)

    # Load existing config if it exists, else create an empty config
    with config_file.open("r") as file:
        try:
            config = json.load(file)
        except json.JSONDecodeError:
            click.echo(click.style("Installing templates...", fg="yellow"))
            config = {}

    # Create the 'tools' key if it does not exist
    if "tools" not in config:
        config["tools"] = {}

    src_path = Path(__file__).parent / "tools/templates"
    for file in src_path.glob("*.yaml"):
        destination = dest_path / file.name

        # Only copy file if it does not exist
        if not destination.exists():
            shutil.copy2(file, dest_path)

            # Update the config file with the copied template
            template_name = file.stem
            config["tools"][template_name] = str(dest_path / file.name)
            click.echo(click.style(f"Installed `{template_name}` template.", fg="green"))

    # Write the updated config back to the file
    with config_file.open("w") as file:
        json.dump(config, file, indent=4)


install_templates()


@click.group()
@click.pass_context
@click.version_option()
def cli():
    pass


def common_options(function):
    """
    Common options for all commands.
    """

    @wraps(function)
    @click.option("--emoji", is_flag=True, help="Add emotions and emojis.")
    @click.option(
        "-m",
        "--model",
        default=DEFAULT_MODEL,
        help="The model to use for the requests.",
        callback=validate_model_name,
    )
    @click.option(
        "--temperature",
        callback=validate_temperature,
        default=1,
        type=float,
        help="The temperature to use for the requests.",
        show_default=True,
    )
    @click.option(
        "--tokens",
        is_flag=True,
        help=("Count the number of tokens in the prompt, and display the cost of the request."),
    )
    @click.option(
        "--no-stream",
        is_flag=True,
        default=False,
        help="Disable the streaming of the response.",
    )
    @click.option(
        "--raw",
        "-r",
        is_flag=True,
        default=False,
        help="Disable colors and formatting, and print the raw response.",
    )
    @click.option(
        "--debug",
        is_flag=True,
        default=False,
        help="Print debug information.",
    )
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


@cli.command()
@click.argument("words", nargs=-1, required=False)
@click.pass_context
@common_options
def thesaurus(ctx, model, emoji, words, temperature, tokens, no_stream, raw, debug):
    """
    This is the thesaurus command. It requires a word as input, either as an argument or from stdin.
    The command will use the given word to find synonyms and antonyms.

    Example usage: thesaurus [word]
    """
    process_command(
        ctx,
        "thesaurus",
        model,
        emoji,
        words,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("sentence", nargs=-1, required=False)
@click.pass_context
@common_options
def translate(ctx, model, emoji, sentence, temperature, tokens, no_stream, raw, debug):
    """
    Translate a word or sentence.
    """
    process_command(
        ctx,
        "translate",
        model,
        emoji,
        sentence,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("word", nargs=-1, required=False)
@click.pass_context
@common_options
def define(ctx, model, emoji, word, temperature, tokens, no_stream, raw, debug):
    """
    Get a definition for a word.
    """
    process_command(ctx, "define", model, emoji, word, temperature, tokens, no_stream, raw, debug)


@cli.command()
@click.argument("text", nargs=-1, required=False)
@click.pass_context
@common_options
def proofread(ctx, model, emoji, text, temperature, tokens, no_stream, raw, debug):
    """
    Proofread a piece of text.
    """
    process_command(
        ctx, "proofread", model, emoji, text, temperature, tokens, no_stream, raw, debug
    )


@cli.command()
@click.argument("topic", nargs=-1, required=False)
@click.pass_context
@common_options
def lessonize(ctx, model, emoji, topic, temperature, tokens, no_stream, raw, debug):
    """
    Create a lesson from a piece of text.
    """
    process_command(
        ctx,
        "lessonize",
        model,
        emoji,
        topic,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("file", type=click.File("r"), required=False)
@click.pass_context
@common_options
def commitgen(ctx, model, emoji, file, temperature, tokens, no_stream, raw, debug):
    """
    This is the commitgen command. It is used in a git repository.

    The command will generate a detailed commit message based on the changes detected by `git diff --staged`.

    Optionally, it can take entire files to provide more context.

    Example usage: commitgen myfile.py
    """
    # Check if we are in a git repository
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"])
    except subprocess.CalledProcessError:
        # No need to print the error message as it is already printed by git
        sys.exit(1)

    # Check if there are staged changes
    try:
        diff_output = subprocess.check_output(["git", "diff", "--staged"]).decode("utf-8")
    except subprocess.CalledProcessError as error:
        click.echo(click.style(f"Error occurred: {error}", fg="red"), err=True)
        sys.exit(1)
    else:
        if not diff_output:
            click.echo("No staged changes to commit.")
            sys.exit(0)

    if file:
        file_content = file.read()
        prompt_input = diff_output + "\n---\n" + file_content
    else:
        prompt_input = str(diff_output)

    # If *not* in an interactive shell, just generate the commit message and exit
    if not sys.stdout.isatty():
        commit_message = process_command(
            ctx,
            template="commitgen",
            emoji=emoji,
            model=model,
            prompt_input=prompt_input,
            temperature=temperature,
            tokens=tokens,
            no_stream=True,
            raw=raw,
            debug=debug,
        )
        sys.exit(0)

    # If in an interactive shell, ask the user if they want to use the generated commit message
    click.echo("Generating commit message...\n---\n\n")

    commit_message = process_command(
        ctx,
        template="commitgen",
        emoji=emoji,
        model=model,
        prompt_input=prompt_input,
        temperature=temperature,
        tokens=tokens,
        no_stream=no_stream,
        raw=raw,
        debug=debug,
    )

    # Get only the content of the ChatGPT request
    try:
        commit_message = commit_message[0].strip()
    except IndexError as error:
        click.echo(click.style(f"Error occurred: {error}", fg="red"), err=True)
        return
    except TypeError:
        click.echo("No commit message generated. Aborting commit.")
        return

    # Clean `^M` characters
    commit_message = commit_message.replace("\r", "")

    # Ask the user if they want to use the generated commit message
    click.echo("\n---\n")
    choice = click.prompt(
        "Do you want to use this commit message? (yes/edit/no)",
        type=str,
        default="edit",
    )

    choice = choice.lower()
    if choice in ["y", "yes"]:
        choice = "yes"
    elif choice in ["e", "edit"]:
        choice = "edit"
    elif choice in ["n", "no"]:
        choice = "no"
        click.echo(click.style("Aborting commit.", fg="blue"))
        sys.exit(0)
    else:
        click.echo("Invalid option. Aborting commit.")
        sys.exit(1)

    # Write commit message to a tmp file
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, prefix="git_commit_message_", suffix=".txt"
    ) as tmp:
        tmp.write(commit_message)
        tmp_path = tmp.name

    # Open git commit with tmp file as template
    try:
        if choice == "yes":
            subprocess.run(["git", "commit", "-F", tmp_path], check=True)
        elif choice == "edit":
            subprocess.run(["git", "commit", "-e", "-t", tmp_path], check=True)
    except subprocess.CalledProcessError as error:
        click.echo(click.style(f"Error occurred: {error}", fg="red"), err=True)
    finally:
        os.remove(tmp_path)


@cli.command()
@click.argument("file_to_review", type=click.File("r"), required=False)
@click.pass_context
@common_options
def codereview(ctx, model, emoji, file_to_review, temperature, tokens, no_stream, raw, debug):
    """
    Generate a code review for a given file.

    Example usage: cat file.py | codereview --emoji
    """
    process_command(
        ctx,
        "codereview",
        model,
        emoji,
        file_to_review,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("source", nargs=-1, required=False)
@click.pass_context
@common_options
def summarize(ctx, model, emoji, source, temperature, tokens, no_stream, raw, debug):
    """
    Summarize the text, the content of a given file, or a webpage (provided as URL).
    """
    template = "summarize"
    source_str: str = " ".join(source)

    prompt_input: str = ""

    # Determine what kind of source we are dealing with
    if video_summarization.is_youtube_video(source_str):  # YouTube video
        # Fetch the transcript of the YouTube video
        transcript: list[dict] = video_summarization.get_transcript(source_str)
        # Format the transcript
        prompt_input = video_summarization.format_transcript(transcript)
        # Use the video summarization template for the prompt
        template = "video_summarization"
    elif validators.url(source_str):  # Webpage (hopefully)
        try:
            # Fetch the content of the webpage
            source_content = requests.get(source_str, timeout=5).text
        except requests.RequestException as error:
            click.echo(click.style("Error occurred:", fg="red") + f" {error}", err=True)
            sys.exit(1)
        else:
            prompt_input = strip_tags(input=source_content, minify=True)
    else:
        # Read the content from `stdin`
        if source:
            content = "".join(source)
            prompt_input += content

    process_command(
        ctx,
        template,
        model,
        emoji,
        prompt_input,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("work_to_critique", nargs=-1, required=False)
@click.pass_context
@common_options
def critique(ctx, model, emoji, work_to_critique, temperature, tokens, no_stream, raw, debug):
    """
    Generate a critique for a given piece of work.
    """
    process_command(
        ctx,
        "critique",
        model,
        emoji,
        work_to_critique,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("topic", nargs=-1, required=False)
@click.pass_context
@common_options
def pathlearner(ctx, model, emoji, topic, temperature, tokens, no_stream, raw, debug):
    """
    Provide a study plan for a given topic.
    """
    process_command(
        ctx,
        "pathlearner",
        model,
        emoji,
        topic,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("concept", nargs=-1, required=False)
@click.pass_context
@common_options
def explain(ctx, model, emoji, concept, temperature, tokens, no_stream, raw, debug):
    """
    Explain a concept.
    """
    process_command(
        ctx,
        "explain",
        model,
        emoji,
        concept,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("mood", nargs=-1, required=False)
@click.pass_context
@common_options
def cheermeup(ctx, model, emoji, mood, temperature, tokens, no_stream, raw, debug):
    """
    Cheer you up based on your mood.
    """
    process_command(
        ctx, "cheermeup", model, emoji, mood, temperature, tokens, no_stream, raw, debug
    )


@cli.command()
@click.argument("study_material", nargs=-1, required=False)
@click.pass_context
@common_options
def study(ctx, model, emoji, study_material, temperature, tokens, no_stream, raw, debug):
    """
    Generate study material for a topic or from the content of the content of a file.
    """
    process_command(
        ctx,
        "study",
        model,
        emoji,
        study_material,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.argument("library_name", nargs=-1, required=False)
@click.pass_context
@common_options
def teachlib(ctx, model, emoji, library_name, temperature, tokens, no_stream, raw, debug):
    """
    Teach a library.
    """
    process_command(
        ctx,
        "teachlib",
        model,
        emoji,
        library_name,
        temperature,
        tokens,
        no_stream,
        raw,
        debug,
    )


@cli.command()
@click.pass_context
@click.option("--reset", is_flag=True, help="Reset the name and the date of birth.")
@common_options
def life(ctx, reset, model, emoji, temperature, tokens, no_stream, raw, debug):
    """
    Comment on the remaining lifespan of a person.
    """
    template_file = get_template_content("life")
    user_info = template_file["user_info"]

    if user_info["name"] is None or reset:
        user_name = click.prompt("What is your name?", type=str)
    else:
        user_name = user_info["name"]

    while True:
        try:
            if user_info["date_of_birth"] is None or reset:
                date_of_birth_str = click.prompt(
                    "What is your date of birth? (YYYY-MM-DD)", type=str
                )
            else:
                date_of_birth_str = user_info["date_of_birth"]
            date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d")

        except ValueError:
            click.echo("Please enter a valid date.")
        else:
            break

    life_expectancy = user_info["life_expectancy"]
    system = template_file["system"]

    # Update the template file
    template_file["user_info"]["name"] = user_name
    template_file["user_info"]["date_of_birth"] = date_of_birth_str
    template_path = TEMPLATES_DIR / "life.yaml"
    with open(template_path, "w", encoding="UTF-8") as file:
        yaml.dump(template_file, file, default_flow_style=False)

    remaining_days = life_expectancy - (datetime.now() - date_of_birth).days
    percentage = f"{(remaining_days / life_expectancy) * 100:.2f}"

    system = f"{system}".format(
        user_name=user_name, remaining_days=remaining_days, percentage=percentage
    )

    prepare_and_generate_response(
        system=system,
        template="",  # No template for this command
        model=model,
        emoji=True,
        prompt_input="",
        temperature=temperature,
        tokens=tokens,
        no_stream=no_stream,
        raw=raw,
        debug=debug,
    )


def process_command(
    ctx,
    template: str,
    model: str,
    emoji: bool,
    prompt_input: str,
    temperature: float,
    tokens: bool,
    no_stream: bool,
    raw: bool,
    debug: bool,
):
    """
    Process a given command using a specific template and optional lines.
    """
    if template in ["summarize", "commitgen", "video_summarization"]:
        prompt_input = "".join(prompt_input).strip()
    else:
        prompt_input = " ".join(prompt_input).strip()

    if not prompt_input:
        if not sys.stdin.isatty():
            prompt_input = sys.stdin.read()
        elif sys.stdin.isatty():
            click.echo(
                click.style(
                    (
                        "You can paste your prompt below. Press <Enter> to"
                        " skip a line.\nOnce you've done, press Ctrl+D to send it."
                    ),
                    fg="yellow",
                )
                + "\n---"
            )
            prompt_input = sys.stdin.read().strip()
            click.echo()

    if not sys.stdout.isatty():
        no_stream = True

    return prepare_and_generate_response(
        system=None,
        template=template,
        model=model,
        prompt_input=prompt_input,
        emoji=emoji,
        temperature=temperature,
        tokens=tokens,
        no_stream=no_stream,
        raw=raw,
        debug=debug,
    )


if __name__ == "__main__":
    cli()
