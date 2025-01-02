# IP FETCH - Android APK Generation Guide

## Prerequisites

### Windows
1. Python 3.8+
2. pip
3. Java Development Kit (JDK)

### Installation Steps

#### 1. Install Required Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt
pip install buildozer kivy kivymd pillow

# Additional system dependencies might be required
```

#### 2. Generate App Assets
```bash
# Create app icon and splash screen
python create_assets.py
```

#### 3. Build APK

##### Option 1: Using Generate Script
```bash
python generate_apk.py
```

##### Option 2: Manual Buildozer
```bash
# Clean previous builds
buildozer android clean

# Build debug APK
buildozer android debug
```

## Troubleshooting

### Common Issues
- Ensure all dependencies are installed
- Check Python and Java versions
- Verify Android SDK paths

### Dependency Problems
- Update pip: `python -m pip install --upgrade pip`
- Reinstall dependencies: `pip install -r requirements.txt --upgrade`

## APK Location
After successful build, find your APK in:
- `bin/` directory
- Filename: `ip_fetch-*-debug.apk`

## Recommended Development Environment
- Linux/Ubuntu (Recommended)
- Windows Subsystem for Linux (WSL)
- Virtual Machine with Linux

## Notes
- First build may take 15-30 minutes
- Subsequent builds are faster
- Requires stable internet connection

## Supported Android Versions
- Minimum: Android 7.0 (API 24)
- Target: Android 11 (API 30)

## Troubleshooting Contacts
- GitHub Issues
- Project Maintainers

## License
MIT License
