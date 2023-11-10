#!/usr/bin/env bash

# This script replaces specified patterns in .po and .pot files
# Usage: ./replace_locale_paths.sh <pattern_to_replace> <replacement>

# Validate input arguments
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <pattern_to_replace> <replacement>"
  exit 1
fi

# Assign arguments to variables
pattern_to_replace="$1"
replacement_pattern="$2"

# Function to replace and log changes
replace_and_log() {
  local file_path="$1"
  local temporary_file

  # Create a temporary file
  if ! temporary_file=$(mktemp); then
    echo "Error: Failed to create a temporary file."
    exit 1
  fi

  # Process each line in the file
  while IFS= read -r line; do
    if [[ "$line" == *"$pattern_to_replace"* ]]; then
      echo "Old: $line"
      line="${line/$pattern_to_replace/$replacement_pattern}"
      echo "New: $line"
    fi
    echo "$line" >> "$temporary_file"
  done < "$file_path"

  # Replace the original file with the modified one
  if ! mv "$temporary_file" "$file_path"; then
    echo "Error: Failed to replace the original file."
    exit 1
  fi
}

# Export function and variables for 'find -exec'
export -f replace_and_log
export pattern_to_replace
export replacement_pattern

# Find and process .po and .pot files
if ! find . -type f \( -name "*.po" -o -name "*.pot" \) -exec bash -c 'replace_and_log "$0"' {} \; ; then
  echo "Error: No .po or .pot files found."
  exit 1
fi

echo "Paths in .po and .pot files have been replaced."