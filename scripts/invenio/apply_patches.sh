#!/bin/bash


# This script automatet the prcess of applying the patches that is in /patches folder
# .pyenv/versions/3.9.12/envs/kth-rdm-v10-2-venv/lib/python3.9/site-packages/
# Example use: ./scripts/apply_patch.sh $(pwd)/patches/add_to_fixtures.patch

PYTHON_VERSION="3.9.12"
PYTHON_LIBRARY="3.9"
VIRTUAL_ENV="kth-rdm-v10-2-venv"
# VIRTUAL_ENV="kth-rdm-dev"
PYENV_ROOT="$HOME/.pyenv"
PYTHON_PATH="$PYENV_ROOT/versions/$PYTHON_VERSION"
VIRTUAL_ENV_PATH="$PYTHON_PATH/envs/$VIRTUAL_ENV"

SITE_PACKAGES_PATH="$VIRTUAL_ENV_PATH/lib/python$PYTHON_LIBRARY/site-packages"

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
  echo "pyenv not found. Please install it first."
  exit 1
fi

# Check for the given Python version
if [[ ! -d "$PYTHON_PATH" ]]; then
  echo "Python version $PYTHON_VERSION is not installed in pyenv."
  exit 1
fi

# Check for the given virtual environment
if [[ ! -d "$VIRTUAL_ENV_PATH" ]]; then
  echo "Virtual environment '$VIRTUAL_ENV' is not found."
  exit 1
fi

# Change to the specified directory or exit
cd "$SITE_PACKAGES_PATH" || exit 1

# Check for the patch file argument
if [[ -z "$1" ]]; then
  echo "Please provide a full path to the .patch file as an argument."
  exit 1
fi

echo Current dir: $(pwd)

# Apply the patch
patch -p1 -i "$1"

# Undo the patch
# patch -R -p1 -i "$1"

# Check if the patch was applied successfully
if [[ $? -eq 0 ]]; then
  echo "Patch applied successfully."
else
  echo "Failed to apply patch."
  exit 1
fi
