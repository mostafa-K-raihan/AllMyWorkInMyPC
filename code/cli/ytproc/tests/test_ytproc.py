import os
from unittest.mock import MagicMock, patch

import pytest

from ytproc import check_ffmpeg, convert_to_audio, download_video


def test_check_ffmpeg_available():
    """Test that check_ffmpeg doesn't raise when ffmpeg is available"""
    with patch("shutil.which") as mock_which:
        mock_which.return_value = "/usr/bin/ffmpeg"
        check_ffmpeg()  # Should not raise


def test_check_ffmpeg_not_available():
    """Test that check_ffmpeg raises when ffmpeg is not available"""
    with patch("shutil.which") as mock_which:
        mock_which.return_value = None
        with pytest.raises(SystemExit):
            check_ffmpeg()


def test_download_video():
    """Test video download functionality"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    output_path = "test_output.mp4"

    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_ydl_instance

        download_video(url, output_path)

        mock_ydl_instance.download.assert_called_once_with([url])


def test_convert_to_audio():
    """Test audio conversion functionality"""
    video_path = "test_video.mp4"
    audio_path = "test_audio.mp3"

    with patch("pydub.AudioSegment") as mock_audio:
        mock_audio_instance = MagicMock()
        mock_audio.from_file.return_value = mock_audio_instance

        convert_to_audio(video_path, audio_path)

        mock_audio.from_file.assert_called_once_with(video_path)
        mock_audio_instance.export.assert_called_once_with(audio_path, format="mp3")


def test_cli_download_video():
    with patch("ytproc.download_video") as mock_download:
        from ytproc import cli

        with patch(
            "sys.argv",
            [
                "ytproc.py",
                "download",
                "https://www.youtube.com/watch?v=test",
                "-o",
                "output",
            ],
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
