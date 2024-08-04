import pytest
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled

from lmtoolbox.video_summarization import (
    YOUTUBE_URL_PATTERN,
    format_transcript,
    get_transcript,
    is_youtube_video,
)


# Test cases for is_youtube_video function
@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", True),
        (" https://www.youtube.com/watch?v=dQw4w9WgXcQ ", True),  # with spaces around
        ("https://youtu.be/dQw4w9WgXcQ", True),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", True),
        ("https://youtube.com/shorts/dQw4w9WgXcQ", True),
        ("https://youtube.com/live/dQw4w9WgXcQ", True),
        ("https://www.youtube.com", False),
        ("https://www.google.com", False),
        ("https://www.dailymotion.com/video/x8i1ffw", False),
        ("not a URL", False),
        ("", False),
    ],
)
def test_is_youtube_video(url, expected):
    assert is_youtube_video(url) == expected


def test_is_youtube_video_none_input():
    with pytest.raises(AttributeError):
        is_youtube_video(None)


@pytest.mark.parametrize(
    "youtube_url, expected",
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtube.com/live/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ],
)
def test_extract_youtube_video_id(youtube_url, expected):
    video_id = YOUTUBE_URL_PATTERN.match(youtube_url).group("video_id")
    assert video_id == expected


# Testing `get_transcript()` function when the YouTube video has transcripts disabled.


@pytest.fixture
def youtube_video_url_with_transcripts_disabled():
    """URL for a YouTube video with transcripts disabled."""
    return "https://youtu.be/_Tp8HQ7eVx0"


def assert_transcript_disabled(capsys, excinfo):
    # Ensure `TranscriptsDisabled` was raised before `SystemExit`.
    assert isinstance(excinfo.value.__context__, TranscriptsDisabled)

    # Check the error message is as expected.
    captured = capsys.readouterr()
    assert "An error occurred: Transcripts are disabled for this video" in captured.err

    # Check that the exit code is `1`.
    assert excinfo.value.code == 1


@pytest.mark.real
def test_youtube_transcript_disabled_real(
    youtube_video_url_with_transcripts_disabled, capsys
):
    """
    Test the `get_transcript()` function when the YouTube video has transcripts disabled.

    This test uses the real `youtube_transcript_api` package.
    Therefore, this test takes more time to run.
    """
    # Call `get_transcript()` and expect it to raise `SystemExit`.
    with pytest.raises(SystemExit) as excinfo:
        get_transcript(youtube_video_url_with_transcripts_disabled)
    assert_transcript_disabled(capsys, excinfo)


@pytest.mark.mock
def test_youtube_transcript_disabled_mocked(
    monkeypatch, youtube_video_url_with_transcripts_disabled, capsys
):
    """
    Test the `get_transcript()` function when the YouTube video has transcripts disabled.

    As a mock, the `youtube_transcript_api` package is not used.
    Therefore, this test runs faster.
    """

    # Mock the `youtube_transcript_api.YouTubeTranscriptApi.list_transcripts()` function.
    def mock_get_transcript(_):
        raise TranscriptsDisabled("Mocked `TranscriptsDisabled` error")

    monkeypatch.setattr(
        "youtube_transcript_api.YouTubeTranscriptApi.list_transcripts",
        mock_get_transcript,
    )

    # Call `get_transcript()` and expect it to raise `SystemExit`.
    with pytest.raises(SystemExit) as excinfo:
        get_transcript(youtube_video_url_with_transcripts_disabled)
    assert_transcript_disabled(capsys, excinfo)


# Testing `get_transcript()` function when the YouTube video has no transcripts for the requested languages.


@pytest.fixture
def youtube_video_url_with_no_transcripts_for_english():
    """URL for a YouTube video with no English transcripts. Only French transcripts."""
    return "https://youtu.be/_XJsAQsT0Bo"


def assert_transcript_for_requested_language_not_found(transcript, capsys):
    # Since it should fallback to any available transcript.
    assert transcript is not None
    assert isinstance(transcript, list)
    assert len(transcript) > 0


@pytest.mark.real
def test_youtube_transcript_for_requested_language_not_found_real(
    youtube_video_url_with_no_transcripts_for_english, capsys
):
    """
    Test the `get_transcript()` function when the YouTube video has no transcripts for the requested languages.

    This test uses the real `youtube_transcript_api` package.
    Therefore, this test takes more time to run.
    """
    transcript = get_transcript(
        youtube_video_url_with_no_transcripts_for_english, languages=["en"]
    )
    assert_transcript_for_requested_language_not_found(transcript, capsys)


@pytest.mark.mock
def test_youtube_transcript_for_requested_language_not_found_mock(
    youtube_video_url_with_no_transcripts_for_english, capsys, monkeypatch
):
    """
    Test the `get_transcript()` function when the YouTube video has no transcripts for the requested languages.

    As a mock, the `youtube_transcript_api` package is not used.
    Therefore, this test runs faster.
    """

    def mock_list_transcripts(_):
        class MockTranscript:
            is_generated = True
            language_code = "fr"

            def fetch(self):
                return [{"text": "Mocked French transcript"}]

        class MockTranscriptList:
            def find_transcript(self, languages):
                raise NoTranscriptFound(
                    "dQw4w9WgXcQ",  # mock video_id
                    languages,
                    {"fr": "French transcript available"},
                )

            def __iter__(self):
                yield MockTranscript()

        return MockTranscriptList()

    monkeypatch.setattr(
        "youtube_transcript_api.YouTubeTranscriptApi.list_transcripts",
        mock_list_transcripts,
    )

    transcript = get_transcript(
        youtube_video_url_with_no_transcripts_for_english, languages=["en"]
    )
    assert_transcript_for_requested_language_not_found(transcript, capsys)


def test_format_transcript_without_timecode():
    transcript = [
        {"text": "Hello world!", "start": 0.0, "duration": 2.0},
        {"text": "This is a test.", "start": 2.0, "duration": 4.0},
    ]
    expected = "Hello world! This is a test."
    assert expected == format_transcript(transcript, timecode=False)


def test_format_transcript_with_timecode():
    transcript = [
        {"text": "Hello world!", "start": 0.0, "duration": 2.0},
        {"text": "This is a test.", "start": 2.0, "duration": 4.0},
    ]
    expected = "|0.0| Hello world! |2.0| This is a test."
    assert expected == format_transcript(transcript, timecode=True)
