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

## Building the Binary

To create a standalone executable:

```bash
# Clone the repository
git clone https://github.com/yourusername/ytproc.git
cd ytproc

# Build the binary
./scripts/build_binary.sh
```

The executable will be created in the `dist` directory. You can then copy it to your desired location:

```bash
# Copy to a directory in your PATH (e.g., /usr/local/bin)
sudo cp dist/ytproc /usr/local/bin/
```

## Usage

### Interactive Mode (Default)
Simply run the program without any arguments:
```bash
ytproc
```

### Command-line Mode
Use the `-c` or `--cli` flag for command-line mode:
```bash
# Download video
ytproc -c https://youtube.com/watch?v=VIDEO_ID -o output.mp4

# Download audio
ytproc -c https://youtube.com/watch?v=VIDEO_ID -a -o output.mp3
```

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
