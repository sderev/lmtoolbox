from functools import wraps
from pathlib import Path
import os
import re
import requests
import subprocess
import sys
import tempfile

import click
import validators
from strip_tags.lib import strip_tags

from lmt_cli.lib import *
from lmt_cli.cli import VALID_MODELS


def validate_model_name(ctx, param, value):
    """
    Validates the model name parameter.
    """
    model_name = value.lower()
    if model_name in VALID_MODELS:
        return VALID_MODELS[model_name]
    elif model_name in VALID_MODELS.values():
        return model_name
    else:
        raise click.BadParameter(f"Invalid model: {model_name}")


def validate_temperature(ctx, param, value):
    """
    Validates the temperature parameter.
    """
    if 0 <= value <= 2:
        return value
    else:
        raise click.BadParameter("Temperature must be between 0 and 2.")


@click.group()
@click.pass_context
@click.version_option()
def cli():
    pass


def common_options(f):
    @wraps(f)
    @click.option("--emoji", is_flag=True, help="Add emotions and emojis.")
    @click.option(
        "-m",
        "--model",
        default="gpt-3.5-turbo",
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
        help=(
            "Count the number of tokens in the prompt, and display the cost of the"
            " request."
        ),
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
        return f(*args, **kwargs)

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
    process_command(
        ctx, "define", model, emoji, word, temperature, tokens, no_stream, raw, debug
    )


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

    The command will generate a detailed commit message based on the changes detected by 'git diff --staged'.

    Optionally, it can take entire files to provide more context.

    Example usage: commitgen myfile.py
    """
    # Check if we are in a git repository
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"])
    except subprocess.CalledProcessError as error:
        click.echo(f"{click.style('Error occurred: {error}', fg='red')}", err=True)
        return

    # Check if there are staged changes
    try:
        diff_output = subprocess.check_output(["git", "diff", "--staged"])
    except subprocess.CalledProcessError as error:
        click.echo(f"{click.style('Error occurred: {error}', fg='red')}", err=True)
        return

    if file:
        file_content = file.read()
        prompt_input = diff_output + "\n---\n" + file_content
    else:
        prompt_input = str(diff_output)

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
    commit_message = commit_message[0].strip()

    # Clean `^M` characters
    commit_message = commit_message.replace("\r", "")

    # click.echo(commit_message) #TODO: delete?
    click.echo("\n---\n")

    choice = click.prompt(
        "Do you want to use this commit message? (yes/edit/no)",
        type=str,
        default="edit",
    )

    choice = choice.lower()
    if choice in ["y", "yes", ""]:
        choice = "yes"
    elif choice in ["e", "edit"]:
        choice = "edit"
    elif choice in ["n", "no"]:
        choice = "no"
        click.echo(click.style("Aborting commit.", fg="blue"))
        return
    else:
        click.echo("Invalid option. Aborting commit.")
        return

    # Write commit message to a temp file
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, prefix="git_commit_message_", suffix=".txt"
    ) as temp:
        temp.write(commit_message)
        temp_path = temp.name

    # Open git commit with temp file as template
    try:
        if choice == "yes":
            subprocess.run(["git", "commit", "-F", temp_path])
        elif choice == "edit":
            subprocess.run(["git", "commit", "-e", "-t", temp_path])
    finally:
        os.remove(temp_path)


@cli.command()
@click.argument("file_to_review", type=click.File("r"), required=False)
@click.pass_context
@common_options
def codereview(
    ctx, model, emoji, file_to_review, temperature, tokens, no_stream, raw, debug
):
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
    source_str = " ".join(source)

    prompt_input = ""

    if is_valid_url(source_str):
        source_content = requests.get(source_str).text
        prompt_input = strip_tags(input=source_content, minify=True)
    else:
        if source:
            content = "".join(source)
            prompt_input += content

    process_command(
        ctx,
        "summarize",
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
def critique(
    ctx, model, emoji, work_to_critique, temperature, tokens, no_stream, raw, debug
):
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
def study(
    ctx, model, emoji, study_material, temperature, tokens, no_stream, raw, debug
):
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
def teachlib(
    ctx, model, emoji, library_name, temperature, tokens, no_stream, raw, debug
):
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
    if not prompt_input:
        if not sys.stdin.isatty():
            prompt_input = sys.stdin.read()
        elif sys.stdin.isatty():
            click.echo(
                click.style(
                    (
                        "You can paste your prompt below. Press <Enter> to"
                        " validate.\nOnce you've done, press Ctrl+D to send it."
                    ),
                    fg="yellow",
                )
                + "\n---"
            )
            prompt_input = sys.stdin.read()
            click.echo()
    prompt_input = "".join(prompt_input).rstrip()

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


def is_valid_url(url):
    return validators.url(url)


if __name__ == "__main__":
    cli()
