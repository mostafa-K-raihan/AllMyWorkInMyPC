#!/bin/bash

# Function to show usage
show_usage() {
    echo "Usage: $0 [local|ci]"
    echo "  local: Use local config (auto-fix)"
    echo "  ci:    Use CI config (check-only)"
    exit 1
}

# Check if argument is provided
if [ $# -ne 1 ]; then
    show_usage
fi

# Switch based on argument
case "$1" in
    "local")
        cp .pre-commit-config.local.yaml .pre-commit-config.yaml
        echo "Switched to local config (auto-fix)"
        ;;
    "ci")
        cp .pre-commit-config.yaml .pre-commit-config.yaml
        echo "Switched to CI config (check-only)"
        ;;
    *)
        show_usage
        ;;
esac

# Reinstall pre-commit hooks
pre-commit clean
pre-commit install
