#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Version
VERSION="1.0.0"

# Function to print colored messages
print_message() {
    echo -e "${BLUE}[BUILD]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to build for a specific platform
build_platform() {
    local GOOS=$1
    local GOARCH=$2
    local SUFFIX=$3
    
    print_message "Building for ${GOOS}/${GOARCH}..."
    
    if [ "$GOOS" = "windows" ]; then
        BINARY="ytproc${SUFFIX}.exe"
    else
        BINARY="ytproc${SUFFIX}"
    fi
    
    GOOS=$GOOS GOARCH=$GOARCH go build -o "dist/${BINARY}" -ldflags="-X 'main.Version=${VERSION}'"
    if [ $? -ne 0 ]; then
        print_error "Failed to build for ${GOOS}/${GOARCH}"
        return 1
    fi
    
    print_success "Built ${BINARY}"
}

# Check if yt-dlp is installed
if ! command -v yt-dlp &> /dev/null; then
    print_error "yt-dlp is not installed. Installing..."
    sudo apt update && sudo apt install -y yt-dlp
fi

# Clean previous build
print_message "Cleaning previous build..."
rm -f ytproc
rm -rf dist/

# Create dist directory
mkdir -p dist

# Run tests
print_message "Running tests..."
go test -v
if [ $? -ne 0 ]; then
    print_error "Tests failed!"
    exit 1
fi

# Check if --release flag is provided
if [ "$1" == "--release" ]; then
    print_message "Building release binaries..."
    
    # Build for various platforms
    build_platform "linux" "amd64" "-linux-amd64"
    build_platform "linux" "arm64" "-linux-arm64"
    build_platform "darwin" "amd64" "-darwin-amd64"
    build_platform "darwin" "arm64" "-darwin-arm64"
    build_platform "windows" "amd64" "-windows-amd64"
    
    print_success "Release builds completed! Check the dist/ directory."
else
    # Regular build for current platform
    print_message "Building for current platform..."
    go build -o ytproc -ldflags="-X 'main.Version=${VERSION}'"
    if [ $? -ne 0 ]; then
        print_error "Build failed!"
        exit 1
    fi
fi

print_success "Build completed successfully!"

# Check if --run flag is provided
if [ "$1" == "--run" ]; then
    print_message "Running program..."
    ./ytproc
fi 
