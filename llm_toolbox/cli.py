import click
from functools import wraps
import os
from pathlib import Path
import subprocess
import pty
import sys
from urllib.parse import urlparse
import tempfile
import re


EMOJI = (
    "Add plenty of emojis as a colorful way to convey emotions in your response 😊."
    " However, don't mention that you use emojis."
)


@click.group()
@click.pass_context
def cli():
    pass


def common_options(f):
    @wraps(f)
    @click.option("--emoji", is_flag=True, help="Add emotions and emojis.")
    @click.option(
        "-m",
        "--model",
        type=click.STRING,
        default="gpt-3.5-turbo",
        help="Choose a model.",
    )
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


@cli.command()
@click.argument("words", nargs=-1, required=False)
@click.pass_context
@common_options
def thesaurus(ctx, model, words, emoji):
    """
    This is the thesaurus command. It requires a word as input, either as an argument or from stdin.
    The command will use the given word to find synonyms and antonyms.

    Example usage: thesaurus [word]
    """
    process_command(ctx, "thesaurus", model, words, emoji)


@cli.command()
@click.argument("sentence", nargs=-1, required=False)
@click.pass_context
@common_options
def translate(ctx, model, sentence, emoji):
    """
    Translate a word or sentence.
    """
    process_command(ctx, "translate", model, sentence, emoji)


@cli.command()
@click.argument("word", nargs=-1, required=False)
@click.pass_context
@common_options
def define(ctx, model, word, emoji):
    """
    Get a definition for a word.
    """
    process_command(ctx, "define", model, word, emoji)


@cli.command()
@click.argument("text", nargs=-1, required=False)
@click.pass_context
@common_options
def proofread(ctx, model, text, emoji):
    """
    Proofread a piece of text.
    """
    process_command(ctx, "proofread", model, text, emoji)


@cli.command()
@click.argument("topic", nargs=-1, required=False)
@click.pass_context
@common_options
def lessonize(ctx, model, topic, emoji):
    """
    Create a lesson from a piece of text.
    """
    process_command(ctx, "lessonize", model, topic, emoji)


@cli.command()
@click.argument("file", type=click.File("r"), required=False)
@click.pass_context
@common_options
def commitgen(ctx, model, file, emoji):
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
        #click.echo(f"Error occurred: {error}", err=True)
        return

    # Check if there are staged changes
    try:
        diff_output = subprocess.check_output(["git", "diff", "--staged"]).decode()
    except subprocess.CalledProcessError as error:
        click.echo(f"Error occurred: {error}", err=True)
        # There are no staged changes
        return

    if file:
        file_content = file.read()
        prompt = diff_output + "\n---\n" + file_content
    else:
        prompt = diff_output

    if emoji:
        prompt += f"\n---\n{EMOJI}"

    command = ["llm", "--template", "commitgen", prompt.encode("utf-8")]
    if model:
        command.extend(["--model", str(model)])
    commit_message = subprocess.check_output(command).decode()

    # Write commit message to a temp file
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, prefix="git_commit_message_", suffix=".txt"
    ) as temp:
        temp.write(commit_message)
        temp_path = temp.name

    # Open git commit with temp file as template
    try:
        subprocess.run(["git", "commit", "-t", temp_path])
    finally:
        os.remove(temp_path)


def codereview(ctx, model, file_to_review, emoji):
    """
    Generate a code review for a given file.

    Example usage: cat file.py | codereview --emoji
    """
    process_command(ctx, "codereview", model, file_to_review, emoji)


@cli.command()
@click.argument("source", nargs=-1, required=False)
@click.pass_context
@common_options
def summarize(ctx, model, source, emoji):
    """
    Summarize the text, the content of a given file, or a webpage (provided as URL).
    """
    # No input from pipe and no argument
    if not source and sys.stdin.isatty():
        with click.Context(summarize) as ctx:
            click.echo(summarize.get_help(ctx), err=True)
        return

    source_str = " ".join(source)

    command = ["llm", "--template", "summarize"]
    if model:
        command.extend(["--model", str(model)])

    prompt = "".encode("utf-8")
    if emoji:
        prompt = f"{EMOJI}\n---\n".encode("utf-8")

    if is_valid_url(source_str):
        curl_cmd = ["curl", "-s", source_str]
        strip_tags_cmd = ["strip-tags", "-m"]

        curl_proc = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE)
        strip_tags_proc = subprocess.Popen(
            strip_tags_cmd, stdin=curl_proc.stdout, stdout=subprocess.PIPE
        )
        llm_proc = subprocess.Popen(
            command, stdin=strip_tags_proc.stdout, stdout=subprocess.PIPE
        )

        # Allow curl_proc to receive a SIGPIPE if strip_tags_proc exits.
        curl_proc.stdout.close()
        # Allow strip_tags_proc to receive a SIGPIPE if llm_proc exits.
        strip_tags_proc.stdout.close()

    else:
        if source:
            content = "".join(source).encode("utf-8")
            prompt += content
            command.append(prompt)

    execute(command)


@cli.command()
@click.argument("work_to_critique", nargs=-1, required=False)
@click.pass_context
@common_options
def critique(ctx, model, work_to_critique, emoji):
    """
    Generate a critique for a given piece of work.
    """
    process_command(ctx, "critique", model, work_to_critique, emoji)


@cli.command()
@click.argument("topic", nargs=-1, required=False)
@click.pass_context
@common_options
def pathlearner(ctx, model, topic, emoji):
    """
    Provide a study plan for a given topic.
    """
    process_command(ctx, "pathlearner", model, topic, emoji)


@cli.command()
@click.argument("concept", nargs=-1, required=False)
@click.pass_context
@common_options
def explain(ctx, model, concept, emoji):
    """
    Explain a concept.
    """
    process_command(ctx, "explain", model, concept, emoji)


@cli.command()
@click.argument("mood", nargs=-1, required=False)
@click.pass_context
@common_options
def cheermeup(mood):
    """
    Cheer you up based on your mood.
    """
    process_command(ctx, "cheermeup", mood)


@cli.command()
@click.argument("study_material", nargs=-1, required=False)
@click.pass_context
@common_options
def study(ctx, model, study_material, emoji):
    """
    Generate study material for a topic or from the content of the content of a file.
    """
    process_command(ctx, "study", model, study_material, emoji)


@cli.command()
@click.argument("library_name", nargs=-1, required=False)
@click.pass_context
@common_options
def teachlib(ctx, model, library_name, emoji):
    """
    Teach a library.
    """
    process_command(ctx, "teachlib", model, library_name, emoji)


def process_command(ctx, command_name, model, prompt, emoji):
    """
    Process a given command using a specific template and optional lines.

    This function forms a command for the Language Learning Model (LLM) using
    a specified command name and optionally lines. The formed command is then executed.
    If no lines are provided, the function attempts to read from the standard input.
    """
    if not prompt and sys.stdin.isatty():
        with click.Context(ctx.command) as ctx:
            click.echo(ctx.command.get_help(ctx), err=True)
        return

    if not prompt:
        prompt = sys.stdin.read().splitlines()

    command = ["llm", "--template", command_name]

    if model:
        command.extend(["--model", str(model)])

    if prompt:
        prompt = "\n".join(prompt)

        if emoji:
            prompt += EMOJI
        command.append(prompt.encode("utf-8"))

    execute(command)


def execute(command):
    """
    Execute a subprocess and print the output in real-time.
    """
    try:
        # Open a pseudo-terminal to interact with the subprocess
        master, slave = pty.openpty()

        process = subprocess.Popen(command, stdout=slave, stderr=subprocess.STDOUT)

        os.close(slave)  # Close the slave pty, otherwise we won't get EOF

        while True:
            try:
                output = os.read(master, 8)  # Read chunks of 8 bytes
                if not output:
                    break
                try:
                    decoded_output = output.decode("utf-8")
                except UnicodeDecodeError as error:
                    decoded_output = output.decode("utf-8", errors="replace")
                    click.echo(f"Error decoding output: {error}", err=True)

                print(output.decode(), end="")
                sys.stdout.flush()
            except OSError:
                break  # Probably the process has ended

        os.close(master)  # Close the master pty too when we're done.

        exit_status = process.wait()
        if exit_status != 0:
            click.echo(f"'{command}' exited with status {exit_status}", err=True)

    except Exception as error:
        click.echo(
            f"Error occurred while executing command:\n{str(error)}",
            err=True,
        )


def is_valid_url(url):
    pattern = r"^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"
    return re.match(pattern, url)


if __name__ == "__main__":
    cli()
