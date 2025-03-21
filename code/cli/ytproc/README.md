# YTPROC - YouTube Video Processing CLI Tool

A command-line tool for downloading YouTube videos and converting them to audio format.

## Features

- Download YouTube videos in best quality
- Convert videos to MP3 audio format
- Progress bars for download and conversion
- Simple and intuitive CLI interface

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Download Video
```bash
python ytproc.py download "https://www.youtube.com/watch?v=VIDEO_ID" -o output
```

### Download and Convert to Audio
```bash
python ytproc.py download "https://www.youtube.com/watch?v=VIDEO_ID" -o output -a
```

### Options

- `-o, --output`: Specify output filename (without extension)
- `-a, --audio-only`: Download and convert to audio only

## Requirements

- Python 3.6+
- FFmpeg (for audio conversion)
- Required Python packages (see requirements.txt)

## Note

Make sure you have FFmpeg installed on your system for audio conversion functionality.
