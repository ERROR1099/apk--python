[app]
title = IP FETCH
package.name = ip_fetch
package.domain = com.networktoolkit
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,kivymd,requests,dnspython,ipwhois,speedtest-cli,ping3,matplotlib,seaborn,pillow

# Orientation and Display
orientation = portrait
fullscreen = 0

# Main application file
p4a.main = main.py

# App Icon and Splash Screen
android.icon = assets/app_icon.png
android.presplash = assets/splash_screen.png

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# Android API and SDK Configuration
android.api = 30
android.minapi = 24
android.sdk = 30
android.ndk = 23b

# App Configurations
android.enable_backup = True
android.archs = arm64-v8a, armeabi-v7a

# App Description
android.meta_data = 
    Network and IP Information Toolkit
    Comprehensive network analysis tools

# App Category
android.manifest_placeholders = 
    category=tools

# Additional Python-for-Android bootstrap
p4a.bootstrap = sdl2

# Windows-specific build configuration
p4a.branch = master
p4a.hook = 
    ADDITIONAL_SETUP_PY_ARGS = ["--disable-static-analysis"]

[buildozer]
log_level = 2
warn_on_root = 1

# Additional Windows build options
p4a.python_version = 3.9
p4a.branch = master
