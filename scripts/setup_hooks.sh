#!/bin/bash

HOOKS_DIR=".git/hooks"
SOURCE_HOOKS_DIR="hooks"

# Ensure .git/hooks exists
mkdir -p "$HOOKS_DIR"

# Copy hooks to .git/hooks
cp "$SOURCE_HOOKS_DIR/pre-commit" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

echo "Git hooks installed successfully."
