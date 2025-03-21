import os
from unittest.mock import MagicMock, patch

import pytest

from ytproc import convert_to_audio, download_video


def test_download_video():
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        # Mock the download method
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance

        # Test the download function
        download_video("https://www.youtube.com/watch?v=test", "test.mp4")

        # Verify that YoutubeDL was called with correct options
        mock_ydl.assert_called_once()
        call_args = mock_ydl.call_args[0][0]
        assert call_args["format"] == "best"
        assert call_args["outtmpl"] == "test.mp4"
        assert call_args["quiet"] is True


def test_convert_to_audio():
    with patch("pydub.AudioSegment.from_file") as mock_from_file, patch(
        "pydub.AudioSegment.export"
    ) as mock_export:
        # Mock the audio conversion
        mock_audio = MagicMock()
        mock_from_file.return_value = mock_audio

        # Test the conversion function
        convert_to_audio("test.mp4", "test.mp3")

        # Verify that the conversion was called with correct parameters
        mock_from_file.assert_called_once_with("test.mp4")
        mock_export.assert_called_once_with("test.mp3", format="mp3")


def test_cli_download_video():
    with patch("ytproc.download_video") as mock_download:
        from ytproc import cli

        with patch(
            "sys.argv",
            ["ytproc.py", "download", "https://www.youtube.com/watch?v=test", "-o", "output"],
        ):
            cli()
            mock_download.assert_called_once_with(
                "https://www.youtube.com/watch?v=test", "output.mp4"
            )


def test_cli_download_audio():
    with patch("ytproc.download_video") as mock_download, patch(
        "ytproc.convert_to_audio"
    ) as mock_convert, patch("os.remove") as mock_remove:
        from ytproc import cli

        with patch(
            "sys.argv",
            [
                "ytproc.py",
                "download",
                "https://www.youtube.com/watch?v=test",
                "-o",
                "output",
                "-a",
            ],
        ):
            cli()
            mock_download.assert_called_once_with(
                "https://www.youtube.com/watch?v=test", "output.mp4"
            )
            mock_convert.assert_called_once_with("output.mp4", "output.mp3")
            mock_remove.assert_called_once_with("output.mp4") 
