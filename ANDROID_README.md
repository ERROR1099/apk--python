# Network Toolkit - Android Deployment Guide

## Prerequisites
- Python 3.8+
- Buildozer
- Android SDK
- Java Development Kit (JDK)

## Setup for Android Packaging

### 1. Install Dependencies
```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade

# Install system dependencies
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    openjdk-11-jdk \
    wget \
    unzip

# Install Python dependencies
pip3 install --upgrade pip
pip3 install buildozer cython
```

### 2. Install Android SDK and NDK
```bash
# Download Android SDK
wget https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip
unzip commandlinetools-linux-8512546_latest.zip
mkdir -p android-sdk/cmdline-tools
mv cmdline-tools android-sdk/cmdline-tools/latest

# Set environment variables
export ANDROID_HOME=$HOME/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# Install SDK components
sdkmanager "platform-tools" "platforms;android-30" "build-tools;30.0.3"
sdkmanager "ndk;23.1.7779620"
```

### 3. Build Android APK
```bash
# Clone the project
git clone [your-repo-url]
cd network-toolkit

# Initialize buildozer
buildozer init

# Build debug APK
buildozer android debug deploy run
```

## Troubleshooting
- Ensure all SDK components are installed
- Check Python and Java versions
- Verify buildozer configuration
- Run with sudo if permission issues occur

## Supported Android Versions
- Minimum: Android 7.0 (API 24)
- Target: Android 11 (API 30)

## Supported Architectures
- ARM 64-bit (arm64-v8a)
- ARM 32-bit (armeabi-v7a)

## Known Issues
- Some network tools may require additional permissions
- Performance varies by device specifications

## Contributing
Report issues or submit pull requests on our GitHub repository.

## License
MIT License
