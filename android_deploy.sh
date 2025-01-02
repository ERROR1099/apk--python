#!/bin/bash

# Android Deployment Script for Network Toolkit

# Check for required tools
command -v buildozer >/dev/null 2>&1 || { 
    echo >&2 "Buildozer is not installed. Please install it first."; 
    exit 1; 
}

# Clean previous builds
echo "Cleaning previous builds..."
buildozer android clean

# Upgrade dependencies
pip install --upgrade -r android_requirements.txt

# Prepare Android package
echo "Preparing Android package..."
buildozer android debug

# Optional: Deploy to connected device
read -p "Deploy to connected device? (y/n): " deploy_choice
if [[ $deploy_choice == "y" ]]; then
    buildozer android deploy
fi

# Optional: Run on device
read -p "Run on connected device? (y/n): " run_choice
if [[ $run_choice == "y" ]]; then
    buildozer android run
fi

echo "Android deployment process complete."
