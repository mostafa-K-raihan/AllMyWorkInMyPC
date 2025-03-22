"""Main entry point for ytproc."""

import argparse
import sys

from .core import download_audio, download_video
from .interactive import run_interactive


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Download YouTube videos and audio")
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument("url", nargs="?", help="YouTube URL to download")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument(
        "-a", "--audio", action="store_true", help="Download audio only"
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    if args.interactive:
        run_interactive()
        return

    if not args.url:
        print("Error: URL is required in command-line mode")
        print("Use --interactive for interactive mode")
        sys.exit(1)

    try:
        if args.audio:
            download_audio(args.url, args.output)
        else:
            download_video(args.url, args.output)
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
