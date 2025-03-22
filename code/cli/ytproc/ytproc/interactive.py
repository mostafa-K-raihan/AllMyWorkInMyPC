"""Interactive CLI interface for ytproc."""

import os
from typing import Optional, Tuple

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .core import download_audio, download_video
from .utils import get_video_info

console = Console()
session = PromptSession()


def display_welcome() -> None:
    """Display the welcome message and main menu."""
    console.print(
        Panel.fit(
            "[bold blue]Welcome to ytproc![/bold blue]\n\n"
            "A simple tool for downloading YouTube videos and audio.",
            title="ytproc v1.0.0",
            border_style="blue",
        )
    )

    table = Table(show_header=False, box=None)
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")

    table.add_row("d", "Download video")
    table.add_row("a", "Download audio")
    table.add_row("h", "Show help")
    table.add_row("q", "Quit program")

    console.print(table)


def get_youtube_url() -> Optional[str]:
    """Prompt for YouTube URL with validation."""
    while True:
        url = Prompt.ask("\nEnter YouTube URL", default="")
        if not url:
            return None

        if "youtube.com" in url or "youtu.be" in url:
            return url
        console.print("[red]Invalid YouTube URL. Please try again.[/red]")


def select_format() -> str:
    """Prompt for output format selection."""
    while True:
        choice = Prompt.ask("\nSelect output format", choices=["1", "2"], default="1")
        return "video" if choice == "1" else "audio"


def get_output_filename(video_id: str, format_type: str) -> str:
    """Generate and prompt for output filename."""
    default_name = f"video-{video_id}.{format_type}"
    return Prompt.ask("\nEnter output filename", default=default_name)


def confirm_download(url: str, format_type: str, output_file: str) -> bool:
    """Show download confirmation dialog."""
    console.print("\n[bold]Download Details:[/bold]")
    console.print(f"URL: {url}")
    console.print(f"Format: {format_type.upper()}")
    console.print(f"Output: {output_file}")

    return Confirm.ask("\nProceed with download?", default=True)


def handle_download(format_type: str) -> None:
    """Handle the download process for either video or audio."""
    url = get_youtube_url()
    if not url:
        return

    try:
        video_info = get_video_info(url)
        output_file = get_output_filename(video_info["id"], format_type)

        if confirm_download(url, format_type, output_file):
            if format_type == "video":
                download_video(url, output_file)
            else:
                download_audio(url, output_file)
            console.print("[green]Download completed successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


def show_help() -> None:
    """Display help information."""
    console.print(
        Panel.fit(
            "[bold]ytproc Help[/bold]\n\n"
            "Commands:\n"
            "  d - Download video\n"
            "  a - Download audio\n"
            "  h - Show this help\n"
            "  q - Quit program\n\n"
            "Usage:\n"
            "  1. Select a command from the main menu\n"
            "  2. Enter the YouTube URL\n"
            "  3. Choose output format (if applicable)\n"
            "  4. Enter output filename or use default\n"
            "  5. Confirm download",
            title="Help",
            border_style="blue",
        )
    )


def run_interactive() -> None:
    """Run the interactive CLI interface."""
    display_welcome()

    while True:
        try:
            command = session.prompt("\nEnter command (h for help): ").lower()

            if command == "q":
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif command == "h":
                show_help()
            elif command == "d":
                handle_download("video")
            elif command == "a":
                handle_download("audio")
            else:
                console.print("[red]Invalid command. Type 'h' for help.[/red]")

        except KeyboardInterrupt:
            continue
        except EOFError:
            break
