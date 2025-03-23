package main

import (
	"testing"
)

func TestProcessVideo(t *testing.T) {
	// Test with invalid URL
	err := processVideo("invalid-url", "", "both", func(line string) {})
	if err == nil {
		t.Error("Expected error for invalid URL, got nil")
	}

	// Test with empty URL
	err = processVideo("", "", "both", func(line string) {})
	if err == nil {
		t.Error("Expected error for empty URL, got nil")
	}

	// Test with invalid download type
	err = processVideo("https://youtube.com/watch?v=123", "", "invalid", func(line string) {})
	if err == nil {
		t.Error("Expected error for invalid download type, got nil")
	}
} 
