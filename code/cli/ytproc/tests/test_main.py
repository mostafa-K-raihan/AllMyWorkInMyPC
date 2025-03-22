"""Tests for the main entry point."""

from unittest.mock import patch

import pytest
from ytproc.__main__ import main, parse_args


def test_parse_args_interactive():
    """Test parsing arguments for interactive mode."""
    with patch("sys.argv", ["ytproc", "-i"]):
        args = parse_args()
        assert args.interactive is True
        assert args.url is None
        assert args.output is None
        assert args.audio is False


def test_parse_args_video_download():
    """Test parsing arguments for video download."""
    with patch(
        "sys.argv", ["ytproc", "https://youtube.com/watch?v=abc123", "-o", "output.mp4"]
    ):
        args = parse_args()
        assert args.interactive is False
        assert args.url == "https://youtube.com/watch?v=abc123"
        assert args.output == "output.mp4"
        assert args.audio is False


def test_parse_args_audio_download():
    """Test parsing arguments for audio download."""
    with patch(
        "sys.argv",
        ["ytproc", "https://youtube.com/watch?v=abc123", "-a", "-o", "output.mp3"],
    ):
        args = parse_args()
        assert args.interactive is False
        assert args.url == "https://youtube.com/watch?v=abc123"
        assert args.output == "output.mp3"
        assert args.audio is True


def test_main_interactive_mode():
    """Test main function in interactive mode."""
    with patch("ytproc.__main__.run_interactive") as mock_run_interactive:
        with patch("sys.argv", ["ytproc", "-i"]):
            main()
            mock_run_interactive.assert_called_once()


def test_main_video_download():
    """Test main function for video download."""
    with patch("ytproc.__main__.download_video") as mock_download_video:
        with patch(
            "sys.argv",
            ["ytproc", "https://youtube.com/watch?v=abc123", "-o", "output.mp4"],
        ):
            main()
            mock_download_video.assert_called_once_with(
                "https://youtube.com/watch?v=abc123", "output.mp4"
            )


def test_main_audio_download():
    """Test main function for audio download."""
    with patch("ytproc.__main__.download_audio") as mock_download_audio:
        with patch(
            "sys.argv",
            ["ytproc", "https://youtube.com/watch?v=abc123", "-a", "-o", "output.mp3"],
        ):
            main()
            mock_download_audio.assert_called_once_with(
                "https://youtube.com/watch?v=abc123", "output.mp3"
            )


def test_main_missing_url():
    """Test main function with missing URL."""
    with patch("sys.argv", ["ytproc"]):
        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)


def test_main_download_error():
    """Test main function handling download error."""
    with patch(
        "ytproc.__main__.download_video", side_effect=Exception("Download failed")
    ):
        with patch("sys.argv", ["ytproc", "https://youtube.com/watch?v=abc123"]):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_called_once_with(1)
