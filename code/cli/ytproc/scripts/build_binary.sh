#!/bin/bash

# Exit on error
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Build the executable
pyinstaller ytproc.spec --clean

# Print success message
echo "Build completed successfully!"
echo "The executable is located at: dist/ytproc" 
