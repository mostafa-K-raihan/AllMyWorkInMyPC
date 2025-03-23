package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/charmbracelet/bubbles/spinner"
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/spf13/cobra"
)

// Custom messages for our program
type downloadProgressMsg string
type downloadCompleteMsg struct{}

var (
	rootCmd = &cobra.Command{
		Use:   "ytproc",
		Short: "YouTube video processor with interactive CLI",
		Long: `ytproc is a command-line tool for downloading and processing YouTube videos.
It provides an interactive interface for easy video downloading and processing.`,
		Run: func(cmd *cobra.Command, args []string) {
			if len(args) > 0 {
				// Command-line mode
				url := args[0]
				outputName := ""
				if len(args) > 1 {
					outputName = args[1]
				}
				processVideo(url, outputName, "both", func(line string) {
					fmt.Println(line)
				})
			} else {
				// Interactive mode
				runInteractive()
			}
		},
	}

	// Styles
	titleStyle = lipgloss.NewStyle().
		Bold(true).
		Foreground(lipgloss.Color("205")).
		MarginBottom(1)

	subtitleStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("241")).
		MarginBottom(1)

	highlightStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("205")).
		Bold(true)

	optionStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("252"))

	selectedStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("205")).
		Bold(true)

	boxStyle = lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("205")).
		Padding(1).
		Align(lipgloss.Left)

	logStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("252")).
		Width(70).
		Border(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("205")).
		Padding(1).
		Align(lipgloss.Left)

	successStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("82")).
		Bold(true)
)

type model struct {
	urlInput     textinput.Model
	outputInput  textinput.Model
	spinner      spinner.Model
	state        string
	err          error
	success      bool
	width        int
	height       int
	downloadLog  []string
	lastUpdate   time.Time
	selectedOption int
	downloadType string // "video", "audio", or "both"
	showBanner   bool
}

func initialModel() model {
	urlInput := textinput.New()
	urlInput.Placeholder = "Enter YouTube URL"
	urlInput.Focus()
	urlInput.Width = 50

	outputInput := textinput.New()
	outputInput.Placeholder = "Enter output filename (optional)"
	outputInput.Width = 50

	s := spinner.New()
	s.Spinner = spinner.Points
	s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))

	return model{
		urlInput:    urlInput,
		outputInput: outputInput,
		spinner:     s,
		state:       "welcome",
		downloadLog: make([]string, 0),
		lastUpdate:  time.Now(),
		downloadType: "both",
		showBanner:  true,
	}
}

func (m model) Init() tea.Cmd {
	return tea.Batch(textinput.Blink, m.spinner.Tick)
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
	case downloadProgressMsg:
		if time.Since(m.lastUpdate) > 100*time.Millisecond {
			newMsg := string(msg)
			if len(m.downloadLog) == 0 || m.downloadLog[len(m.downloadLog)-1] != newMsg {
				m.downloadLog = append(m.downloadLog, newMsg)
				if len(m.downloadLog) > 10 {
					m.downloadLog = m.downloadLog[1:]
				}
			}
			m.lastUpdate = time.Now()
			return m, m.spinner.Tick
		}
		return m, nil
	case downloadCompleteMsg:
		m.success = true
		m.state = "options"
		m.showBanner = true
		return m, nil
	case tea.KeyMsg:
		switch msg.Type {
		case tea.KeyCtrlC, tea.KeyEsc:
			return m, tea.Quit
		case tea.KeyEnter:
			switch m.state {
			case "welcome":
				m.state = "url"
				return m, nil
			case "url":
				m.state = "download_type"
				m.urlInput.Blur()
				return m, nil
			case "download_type":
				m.state = "output"
				m.outputInput.Focus()
				return m, nil
			case "output":
				url := m.urlInput.Value()
				outputName := m.outputInput.Value()
				if url != "" {
					m.state = "processing"
					m.downloadLog = make([]string, 0)
					m.showBanner = false
					return m, tea.Batch(
						m.spinner.Tick,
						func() tea.Msg {
							go func() {
								processVideo(url, outputName, m.downloadType, func(line string) {
									p.Send(downloadProgressMsg(line))
								})
								p.Send(downloadCompleteMsg{})
							}()
							return nil
						},
					)
				}
			case "options":
				switch m.selectedOption {
				case 0: // Download another video
					newModel := initialModel()
					newModel.width = m.width    // Preserve window size
					newModel.height = m.height  // Preserve window size
					newModel.state = "url"
					return newModel, nil
				case 1: // Exit
					return m, tea.Quit
				}
			}
		case tea.KeyUp:
			if m.state == "options" && m.selectedOption > 0 {
				m.selectedOption--
			} else if m.state == "download_type" {
				switch m.downloadType {
				case "both":
					m.downloadType = "audio"
				case "audio":
					m.downloadType = "video"
				case "video":
					m.downloadType = "both"
				}
			}
		case tea.KeyDown:
			if m.state == "options" && m.selectedOption < 1 {
				m.selectedOption++
			} else if m.state == "download_type" {
				switch m.downloadType {
				case "both":
					m.downloadType = "video"
				case "video":
					m.downloadType = "audio"
				case "audio":
					m.downloadType = "both"
				}
			}
		}
	case spinner.TickMsg:
		var spinnerCmd tea.Cmd
		m.spinner, spinnerCmd = m.spinner.Update(msg)
		return m, spinnerCmd
	}

	switch m.state {
	case "url":
		m.urlInput, cmd = m.urlInput.Update(msg)
		cmds = append(cmds, cmd)
	case "output":
		m.outputInput, cmd = m.outputInput.Update(msg)
		cmds = append(cmds, cmd)
	case "processing":
		if !m.success {
			cmds = append(cmds, m.spinner.Tick)
		}
	}

	return m, tea.Batch(cmds...)
}

func (m model) View() string {
	// Container style
	containerStyle := lipgloss.NewStyle().
		Width(m.width).
		Height(m.height).
		Align(lipgloss.Center, lipgloss.Center)

	// Content
	var content strings.Builder

	switch m.state {
	case "welcome":
		content.WriteString(titleStyle.Render("✨ Welcome to YouTube Video Processor ✨") + "\n\n")
		content.WriteString(boxStyle.Width(60).Render(
			"This tool helps you download YouTube videos with ease!\n\n" +
			highlightStyle.Render("Features:") + "\n" +
			"• Download videos in highest quality\n" +
			"• Download audio only\n" +
			"• Custom output filenames\n" +
			"• Interactive UI with real-time progress\n\n" +
			subtitleStyle.Render("Press ENTER to start, ESC to quit"),
		))

	case "url":
		if m.showBanner {
			content.WriteString(titleStyle.Render("✨ YouTube Video Processor ✨") + "\n\n")
		}
		content.WriteString(boxStyle.Width(60).Render(
			subtitleStyle.Render("Enter YouTube URL:") + "\n" +
			m.urlInput.View() + "\n\n" +
			subtitleStyle.Render("Press ENTER to continue"),
		))

	case "download_type":
		if m.showBanner {
			content.WriteString(titleStyle.Render("✨ YouTube Video Processor ✨") + "\n\n")
		}
		content.WriteString(boxStyle.Width(60).Render(
			subtitleStyle.Render("Select Download Type:") + "\n\n" +
			renderOption("Both Video and Audio", m.downloadType == "both") + "\n" +
			renderOption("Video Only", m.downloadType == "video") + "\n" +
			renderOption("Audio Only", m.downloadType == "audio") + "\n\n" +
			subtitleStyle.Render("Use ↑↓ to select, ENTER to continue"),
		))

	case "output":
		if m.showBanner {
			content.WriteString(titleStyle.Render("✨ YouTube Video Processor ✨") + "\n\n")
		}
		content.WriteString(boxStyle.Width(60).Render(
			subtitleStyle.Render("Enter output filename (optional):") + "\n" +
			m.outputInput.View() + "\n\n" +
			subtitleStyle.Render("Press ENTER to start download"),
		))

	case "processing":
		// No banner during processing
		content.WriteString(boxStyle.Width(60).Render(
			highlightStyle.Render("Downloading...") + "\n\n" +
			m.spinner.View() + " " + getProgressStatus(m.downloadLog) + "\n" +
			getProgressBar(m.downloadLog) + "\n\n" +
			subtitleStyle.Render("This may take a few minutes..."),
		))

	case "options":
		if m.showBanner {
			content.WriteString(titleStyle.Render("✨ YouTube Video Processor ✨") + "\n\n")
		}
		content.WriteString(boxStyle.Width(60).Render(
			successStyle.Render("Download Complete!") + "\n\n" +
			renderOption("Download Another Video", m.selectedOption == 0) + "\n" +
			renderOption("Exit", m.selectedOption == 1) + "\n\n" +
			subtitleStyle.Render("Use ↑↓ to select, ENTER to confirm"),
		))
	}

	return containerStyle.Render(content.String())
}

func renderOption(text string, selected bool) string {
	if selected {
		return "► " + selectedStyle.Render(text)
	}
	return "  " + optionStyle.Render(text)
}

// Global program instance for sending messages
var p *tea.Program

func runInteractive() {
	var err error
	p = tea.NewProgram(initialModel(), tea.WithAltScreen())
	if _, err = p.Run(); err != nil {
		fmt.Printf("Error: %v", err)
		os.Exit(1)
	}
}

func processVideo(url, outputName, downloadType string, logCallback func(string)) error {
	// Validate URL
	if url == "" {
		return fmt.Errorf("URL cannot be empty")
	}

	// Validate download type
	validTypes := map[string]bool{
		"both":  true,
		"video": true,
		"audio": true,
	}
	if !validTypes[downloadType] {
		return fmt.Errorf("invalid download type: %s. Must be one of: both, video, audio", downloadType)
	}

	// Check if yt-dlp is installed
	if _, err := exec.LookPath("yt-dlp"); err != nil {
		return fmt.Errorf("yt-dlp is not installed. Please install it first: https://github.com/yt-dlp/yt-dlp#installation")
	}

	// Prepare output filename
	if outputName == "" {
		outputName = "%(title)s.%(ext)s"
	}

	// Build command based on download type
	var cmd *exec.Cmd
	switch downloadType {
	case "audio":
		cmd = exec.Command("yt-dlp",
			"-x",                    // Extract audio
			"--audio-format", "mp3", // Convert to MP3
			"--audio-quality", "0",  // Best quality
			"-o", outputName,
			"--progress",           // Show progress
			"--newline",           // Force new lines
			"--quiet",             // Suppress unnecessary output
			url)
	case "video":
		cmd = exec.Command("yt-dlp",
			"--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", // Best quality MP4
			"-o", outputName,
			"--progress",           // Show progress
			"--newline",           // Force new lines
			"--quiet",             // Suppress unnecessary output
			url)
	default: // "both"
		cmd = exec.Command("yt-dlp",
			"--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", // Best quality MP4
			"-o", outputName,
			"--write-sub",         // Include subtitles if available
			"--progress",          // Show progress
			"--newline",          // Force new lines
			"--quiet",            // Suppress unnecessary output
			url)
	}

	// Set up pipes for output
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return fmt.Errorf("failed to create stdout pipe: %v", err)
	}

	stderr, err := cmd.StderrPipe()
	if err != nil {
		return fmt.Errorf("failed to create stderr pipe: %v", err)
	}

	// Start the command
	if err := cmd.Start(); err != nil {
		return fmt.Errorf("failed to start command: %v", err)
	}

	// Read stdout in a goroutine
	go func() {
		scanner := bufio.NewScanner(stdout)
		for scanner.Scan() {
			line := scanner.Text()
			if strings.Contains(line, "%") || strings.Contains(line, "download") {
				logCallback(line)
			}
		}
	}()

	// Read stderr in a goroutine
	go func() {
		scanner := bufio.NewScanner(stderr)
		for scanner.Scan() {
			line := scanner.Text()
			if strings.Contains(line, "%") || strings.Contains(line, "download") {
				logCallback(line)
			}
		}
	}()

	// Wait for command to complete
	if err := cmd.Wait(); err != nil {
		return fmt.Errorf("command failed: %v", err)
	}

	return nil
}

func getProgressStatus(logs []string) string {
	if len(logs) == 0 {
		return "Initializing..."
	}
	
	lastLog := logs[len(logs)-1]
	
	// Extract percentage if available
	if strings.Contains(lastLog, "of") && strings.Contains(lastLog, "at") {
		return lastLog
	}
	
	return "Processing..."
}

func getProgressBar(logs []string) string {
	if len(logs) == 0 {
		return "[                    ] 0%"
	}
	
	// Find the last log with percentage
	var percentage float64
	for i := len(logs) - 1; i >= 0; i-- {
		if strings.Contains(logs[i], "%") {
			fmt.Sscanf(logs[i], "[download] %f", &percentage)
			break
		}
	}
	
	// Create progress bar
	width := 20
	filled := int((percentage / 100) * float64(width))
	bar := "["
	for i := 0; i < width; i++ {
		if i < filled {
			bar += "="
		} else {
			bar += " "
		}
	}
	bar += fmt.Sprintf("] %.1f%%", percentage)
	
	return bar
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
} 
