"""Tests for the interactive CLI module."""

import pytest
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from rich.console import Console
from ytproc.interactive import (
    get_output_filename,
    get_youtube_url,
    handle_download,
    select_format,
    show_help,
)


@pytest.fixture
def mock_console():
    """Create a mock console for testing."""
    return Console(force_terminal=True, color_system=None)


@pytest.fixture
def mock_input():
    """Create a mock input for testing."""
    return create_pipe_input()


@pytest.fixture
def mock_output():
    """Create a mock output for testing."""
    return DummyOutput()


def test_get_youtube_url_valid(mock_input, mock_output):
    """Test getting a valid YouTube URL."""
    mock_input.send_text("https://youtube.com/watch?v=abc123\n")
    url = get_youtube_url()
    assert url == "https://youtube.com/watch?v=abc123"


def test_get_youtube_url_invalid(mock_input, mock_output):
    """Test getting an invalid YouTube URL."""
    mock_input.send_text("invalid-url\nhttps://youtube.com/watch?v=abc123\n")
    url = get_youtube_url()
    assert url == "https://youtube.com/watch?v=abc123"


def test_get_youtube_url_empty(mock_input, mock_output):
    """Test getting an empty URL (should return None)."""
    mock_input.send_text("\n")
    url = get_youtube_url()
    assert url is None


def test_select_format_video(mock_input, mock_output):
    """Test selecting video format."""
    mock_input.send_text("1\n")
    format_type = select_format()
    assert format_type == "video"


def test_select_format_audio(mock_input, mock_output):
    """Test selecting audio format."""
    mock_input.send_text("2\n")
    format_type = select_format()
    assert format_type == "audio"


def test_get_output_filename(mock_input, mock_output):
    """Test generating output filename."""
    mock_input.send_text("\n")  # Use default
    filename = get_output_filename("abc123", "mp4")
    assert filename == "video-abc123.mp4"


def test_get_output_filename_custom(mock_input, mock_output):
    """Test custom output filename."""
    mock_input.send_text("custom-video.mp4\n")
    filename = get_output_filename("abc123", "mp4")
    assert filename == "custom-video.mp4"


def test_show_help(mock_console, capsys):
    """Test displaying help information."""
    show_help()
    captured = capsys.readouterr()
    assert "ytproc Help" in captured.out
    assert "Commands:" in captured.out
    assert "Usage:" in captured.out


@pytest.mark.parametrize(
    "format_type,expected_func",
    [
        ("video", "download_video"),
        ("audio", "download_audio"),
    ],
)
def test_handle_download(mock_input, mock_output, mocker, format_type, expected_func):
    """Test handling download process."""
    # Mock the necessary functions
    mock_get_video_info = mocker.patch("ytproc.interactive.get_video_info")
    mock_get_video_info.return_value = {"id": "abc123"}
    mock_download = mocker.patch(f"ytproc.interactive.{expected_func}")

    # Simulate user input
    mock_input.send_text("https://youtube.com/watch?v=abc123\n")  # URL
    mock_input.send_text("\n")  # Use default filename
    mock_input.send_text("y\n")  # Confirm download

    # Run the function
    handle_download(format_type)

    # Verify function calls
    mock_get_video_info.assert_called_once_with("https://youtube.com/watch?v=abc123")
    mock_download.assert_called_once_with(
        "https://youtube.com/watch?v=abc123", "video-abc123.mp4"
    )
