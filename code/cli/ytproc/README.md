# YTProc - YouTube Video Processor

A beautiful and interactive CLI tool for downloading YouTube videos with ease. Built with Go and [Charm](https://charm.sh/) libraries.

![YTProc Demo](docs/demo.gif)

## Features

- 🎥 Download videos in highest quality
- 🎵 Extract audio in MP3 format
- 🎨 Beautiful interactive UI with real-time progress
- 📝 Custom output filenames
- 🚀 Easy to use interface

## Installation

### Pre-built Binaries

Download the latest release for your platform from our [releases page](https://github.com/mostafa-K-raihan/ytproc/releases).

```bash
# Linux/macOS
curl -LO https://github.com/mostafa-K-raihan/ytproc/releases/latest/download/ytproc-$(uname -s)-$(uname -m)
chmod +x ytproc-$(uname -s)-$(uname -m)
sudo mv ytproc-$(uname -s)-$(uname -m) /usr/local/bin/ytproc

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://github.com/mostafa-K-raihan/ytproc/releases/latest/download/ytproc-windows-amd64.exe" -OutFile "ytproc.exe"
```

### From Source

Requirements:
- Go 1.21 or higher
- yt-dlp (will be automatically installed if missing)

```bash
# Clone the repository
git clone https://github.com/mostafa-K-raihan/ytproc.git
cd ytproc/code/cli/ytproc

# Install directly (if you have Go installed)
go install github.com/mostafa-K-raihan/ytproc/code/cli/ytproc@latest

# Or build from source
./build.sh
```

## Usage

### Interactive Mode
```bash
ytproc
```

### Command Line Mode
```bash
ytproc <youtube-url> [output-filename]
```

## Code Structure

### Main Components

1. **UI Components** (`main.go:70-110`):
   - Uses [Bubble Tea](https://github.com/charmbracelet/bubbletea) for terminal UI
   - Custom styles defined using [Lip Gloss](https://github.com/charmbracelet/lipgloss)
   - Spinner for loading states

2. **State Management** (`main.go:112-146`):
   ```go
   type model struct {
       urlInput       textinput.Model
       outputInput    textinput.Model
       spinner       spinner.Model
       state         string
       // ... other fields
   }
   ```
   Handles different states: welcome, url input, download type selection, processing, etc.

3. **Download Processing** (`main.go:450-520`):
   ```go
   func processVideo(url, outputName, downloadType string, logCallback func(string)) error {
       // Validates input and handles download using yt-dlp
   }
   ```
   Manages video downloads using yt-dlp with different options based on download type.

4. **Progress Display** (`main.go:522-570`):
   ```go
   func getProgressBar(logs []string) string {
       // Creates visual progress bar
   }
   ```
   Provides real-time download progress with a visual progress bar.

## Development

### Building from Source

1. Clone the repository:
```bash
git clone https://github.com/mostafa-K-raihan/ytproc.git
cd ytproc/code/cli/ytproc
```

2. Run tests:
```bash
./build.sh
```

3. Build for all platforms:
```bash
./build.sh --release
```

### Cross-Platform Building

The release workflow automatically builds binaries for:
- Linux (amd64, arm64)
- macOS (amd64, arm64)
- Windows (amd64)

### Release Process

1. Update version in `build.sh`
2. Create and push a tag:
```bash
git tag ytproc/v1.0.0
git push origin ytproc/v1.0.0
```

This will trigger the GitHub Actions workflow to:
- Run tests
- Build cross-platform binaries
- Create a GitHub release
- Upload the binaries

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Dependencies

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): For video downloading
- [Bubble Tea](https://github.com/charmbracelet/bubbletea): Terminal UI framework
- [Lip Gloss](https://github.com/charmbracelet/lipgloss): Terminal styling
- [Cobra](https://github.com/spf13/cobra): CLI framework

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
