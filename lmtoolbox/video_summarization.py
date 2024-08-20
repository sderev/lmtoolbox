import re
import sys
from typing import Dict, List, Optional

import click
from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)

YOUTUBE_URL_PATTERN = re.compile(
    r"(http(s)?:\/\/)?"  # Optional protocol
    r"(www\.)?"  # Optional www subdomain
    r"youtu(be\.com|\.be)"  # Domain variations
    r"(\/watch\?v=|\/|\/embed\/|\/shorts\/|\/live\/)"  # Path variations
    r"(?P<video_id>[a-zA-Z0-9_-]{11})"  # Video ID capture group
)


def is_youtube_video(url: str) -> bool:
    """
    Checks if the given URL is a valid YouTube video URL.
    Args:
        url (str): The URL to check.
    Returns:
        bool: True if the URL is a valid YouTube video URL, False otherwise.
    """
    if url is None:
        raise (AttributeError("No URL provided."))
    return YOUTUBE_URL_PATTERN.match(url.strip()) is not None


def get_transcript(
    youtube_url: str, languages: List[str] = ["en"]
) -> Optional[List[Dict]]:
    """
    Gets the transcript of a YouTube video.
    Args:
        youtube_url (str): The URL of the YouTube video.
        languages (List[str], optional): The list of languages to search for in the transcript. Defaults to ["en"]. Order of preference is preserved: the first language in the list is the most preferred.
    Returns:
        List[Dict]: The transcript of the video. Only one language is returned. If the specified languages are not found, the function defaults to any generated transcript.

        Each dictionary in the list represents a line in the transcript and has the following keys:

        * start (float): The start time of the line in seconds.
        * duration (float): The duration of the line in seconds.
        * text (str): The text of the line.

        The list of dictionaries looks like this:

        ```
        [
            {
                "start": 0.0,
                "duration": 4.0,
                "text": "Hello, world!"
            },
            {
                "start": 4.0,
                "duration": 3.0,
                "text": "This is a test."
            }
        ]
        ```

    Source for the YouTubeTranscriptApi library documentation:
    https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#api
    """
    youtube_url = youtube_url.strip()
    video_id = YOUTUBE_URL_PATTERN.match(youtube_url).group("video_id")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Select the subtitles for one of the specified languages:
        # manually created if available, fallback to automatically generated.
        transcript = transcript_list.find_transcript(languages)

    except TranscriptsDisabled:
        click.echo(
            f"{click.style('An error occurred', fg='red')}: Transcripts are disabled for this video.",
            err=True,
        )
        sys.exit(1)

    except NoTranscriptFound:
        # If no subtitles are found for the specified languages,
        # default to any generated transcript.
        transcript = next((t for t in transcript_list))

    return transcript.fetch()


def format_transcript(transcript: Dict, timecode: bool = False) -> str:
    """
    Formats the transcript of a YouTube video.
    Args:
        transcript (Dict): The transcript of the video.
        timecode (bool, optional): Whether to include timecodes in the formatted transcript.
            Defaults to False.
    Returns:
        str: The formatted transcript.

        With timecodes, the formatted transcript looks like this:
        "|0.0| Hello, world! |4.0| This is a test."

        Without timecodes, the formatted transcript looks like this:
        "Hello, world! This is a test."
    """
    return " ".join(
        f"|{line['start']}| {line['text']}" if timecode else line["text"]
        for line in transcript
    )
