#!/usr/bin/env python3
import os
import shutil

import click
import yt_dlp
from pydub import AudioSegment
from rich.console import Console
from rich.progress import Progress

console = Console()


def check_ffmpeg():
    """Check if ffmpeg is available in the system"""
    if not shutil.which("ffmpeg"):
        console.print("[red]Error: ffmpeg is not installed or not in PATH")
        console.print("[yellow]Please install ffmpeg using:")
        console.print("[yellow]  Ubuntu/Debian: sudo apt install ffmpeg")
        console.print("[yellow]  macOS: brew install ffmpeg")
        console.print(
            "[yellow]  Windows: Download from https://ffmpeg.org/download.html"
        )
        raise click.Abort()


def download_video(url, output_path):
    """Download YouTube video using yt-dlp"""
    ydl_opts = {
        "format": "best",
        "outtmpl": output_path,
        "quiet": True,
    }

    with Progress() as progress:
        task = progress.add_task("[cyan]Downloading video...", total=None)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        progress.update(task, completed=True)


def convert_to_audio(video_path, audio_path):
    """Convert video to audio using pydub"""
    with Progress() as progress:
        task = progress.add_task("[cyan]Converting to audio...", total=None)
        try:
            video = AudioSegment.from_file(video_path)
            video.export(audio_path, format="mp3")
            progress.update(task, completed=True)
        except Exception as e:
            console.print(f"[red]Error during audio conversion: {str(e)}")
            raise click.Abort()


@click.group()
def cli():
    """YouTube Video Processing CLI Tool"""
    pass


@cli.command()
@click.argument("url")
@click.option(
    "--output", "-o", default="output", help="Output filename (without extension)"
)
@click.option(
    "--audio-only", "-a", is_flag=True, help="Download and convert to audio only"
)
def download(url, output, audio_only):
    """Download YouTube video and optionally convert to audio"""
    try:
        if audio_only:
            check_ffmpeg()  # Check ffmpeg availability before proceeding
            video_path = f"{output}.mp4"
            audio_path = f"{output}.mp3"

            console.print(f"[green]Downloading video from: {url}")
            download_video(url, video_path)

            console.print("[green]Converting to audio...")
            convert_to_audio(video_path, audio_path)

            # Remove video file after conversion
            os.remove(video_path)
            console.print(f"[green]Successfully saved audio to: {audio_path}")
        else:
            video_path = f"{output}.mp4"
            console.print(f"[green]Downloading video from: {url}")
            download_video(url, video_path)
            console.print(f"[green]Successfully saved video to: {video_path}")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        raise click.Abort()


if __name__ == "__main__":
    cli()
