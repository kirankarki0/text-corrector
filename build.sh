#!/bin/bash
set -e
echo "Removing old build artifacts..."
rm -rf build dist
echo "Building the binary with PyInstaller..."
python3 -m PyInstaller realtime_substitute.spec
echo "Build complete. The new binary is in the dist/ directory."
