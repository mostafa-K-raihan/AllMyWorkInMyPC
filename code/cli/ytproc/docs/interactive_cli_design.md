# Interactive CLI Design Document

## Overview
The current CLI requires users to provide all parameters at once through command-line arguments. This can be intimidating for new users and less flexible for interactive use. This design proposes an interactive CLI mode that guides users through the process step by step.

## Requirements

### Core Features
1. Welcome Message
   - Display program name and version
   - Show available commands/options
   - List keyboard shortcuts

2. Interactive Mode
   - Step-by-step input collection
   - Clear prompts and instructions
   - Default values where appropriate
   - Option to go back/change previous inputs

3. Command Shortcuts
   - Quick access to common operations
   - Single-key shortcuts for main functions
   - Consistent shortcut scheme

4. Default Values
   - Smart defaults for output filenames
   - Use video title or ID in defaults
   - Allow user to modify defaults

### User Interface

#### Main Menu
```
Welcome to ytproc v1.0.0!

Available Commands:
1. Download Video (d)
2. Download Audio (a)
3. Help (h)
4. Exit (q)

Enter your choice: _
```

#### Download Flow
1. URL Input
   ```
   Enter YouTube URL (or press Enter to go back): _
   ```

2. Output Format
   ```
   Select output format:
   1. MP4 Video (default)
   2. MP3 Audio
   Enter choice [1]: _
   ```

3. Output Filename
   ```
   Enter output filename (press Enter for default):
   Default: video-{video_id}.mp4
   Filename: _
   ```

4. Confirmation
   ```
   Downloading:
   URL: https://youtube.com/watch?v=...
   Format: MP4
   Output: video-abc123.mp4

   Proceed? [Y/n]: _
   ```

### Keyboard Shortcuts
- `d`: Download video
- `a`: Download audio
- `h`: Show help
- `q`: Quit program
- `b`: Go back to previous step
- `c`: Cancel current operation

### Default Naming Scheme
1. Video downloads: `{video_title}-{video_id}.mp4`
2. Audio downloads: `{video_title}-{video_id}.mp3`
- Remove special characters from title
- Truncate long titles
- Ensure unique filenames

## Implementation Plan

### Phase 1: Core Structure
1. Create interactive menu system
2. Implement basic command handling
3. Add keyboard shortcuts
4. Set up step-by-step flow

### Phase 2: Input Handling
1. URL validation
2. Format selection
3. Filename generation
4. Confirmation system

### Phase 3: User Experience
1. Clear prompts and messages
2. Error handling
3. Progress indicators
4. Help system

### Phase 4: Testing
1. Unit tests for new functions
2. Integration tests
3. User acceptance testing
4. Documentation updates

## Technical Considerations

### Dependencies
- `prompt_toolkit` for enhanced input handling
- `rich` for beautiful terminal output
- `click` for command-line interface

### Error Handling
- Invalid URLs
- Network issues
- File permission problems
- Disk space checks

### Performance
- Minimal overhead from interactive mode
- Quick response to user input
- Efficient filename generation

## Future Enhancements
1. Save user preferences
2. Custom shortcut configuration
3. Batch processing mode
4. History of downloads
5. Download queue management

## Success Criteria
1. Intuitive user interface
2. Clear error messages
3. Efficient workflow
4. Comprehensive help system
5. Robust error handling
