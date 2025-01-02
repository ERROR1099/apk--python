# IP/URL Information Finder

## Overview
This is a Python Kivy-based Android app that provides comprehensive network and security tools, including:

### IP Information
- Detailed geolocation data
- WHOIS information
- DNS record lookup

### Network Tools
- Speed Test (Download/Upload/Ping)
- Ping Tool
- Traceroute

### Security Tools
- SSL Certificate Checker
- Hash Generator (MD5, SHA1, SHA256, Base64)
- UUID Generator

## Prerequisites
- Python 3.8+
- Kivy
- Buildozer (for Android packaging)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For Android deployment:
```bash
pip install buildozer
buildozer init
# Modify buildozer.spec as needed
buildozer android debug deploy run
```

## Features
- Multi-tab interface
- Network performance testing
- Security tool suite
- Works on Android and desktop

## Usage
1. Run the app
2. Choose between IP Info, Network Tools, and Security Tools tabs
3. Enter required information
4. View detailed results

## Network Tools
- Measure internet speed
- Ping hosts
- Trace network routes

## Security Tools
- Check SSL certificates
- Generate cryptographic hashes
- Create unique identifiers

## Dependencies
- Kivy: GUI Framework
- Requests: HTTP Requests
- SpeedTest: Network Speed Testing
- OpenSSL: Certificate Validation
- DNSPython: DNS Queries

## Permissions
Requires internet permission for network queries

## Troubleshooting
- Ensure stable internet connection
- Check input format
- Update dependencies if needed

## License
MIT License
