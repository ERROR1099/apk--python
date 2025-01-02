import os
import subprocess
import sys
import platform

def check_system_requirements():
    """Check system requirements for Android APK generation"""
    print("System Requirements Check:")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.architecture()[0]}")

def install_android_dependencies():
    """Install Android-specific dependencies"""
    android_deps = [
        "buildozer", 
        "cython", 
        "kivy", 
        "python-for-android", 
        "kivymd"
    ]
    
    for dep in android_deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep, "--upgrade"], 
                           check=True, capture_output=True)
            print(f"Successfully installed/upgraded {dep}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {dep}:")
            print(e.stderr.decode())

def generate_assets():
    """Generate app icon and splash screen"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os

        # Create assets directory
        os.makedirs('assets', exist_ok=True)

        # Create App Icon
        def create_app_icon(size=512):
            image = Image.new('RGB', (size, size), color='white')
            draw = ImageDraw.Draw(image)
            
            # Gradient background
            for y in range(size):
                r = int(255 * (1 - y/size))
                g = int(200 * (1 - y/size))
                b = int(100 * (1 - y/size))
                for x in range(size):
                    draw.point((x, y), fill=(r, g, b))
            
            # Network icon elements
            draw.rectangle([size//4, size//4, size*3//4, size*3//4], 
                           outline='white', width=size//20)
            draw.line([size//3, size//2, size*2//3, size//2], 
                      fill='white', width=size//30)
            draw.line([size//2, size//3, size//2, size*2//3], 
                      fill='white', width=size//30)
            
            # Text
            try:
                font = ImageFont.truetype("arial.ttf", size//10)
            except IOError:
                font = ImageFont.load_default()
            
            draw.text((size//4, size*7//8), "IP FETCH", 
                      fill='white', font=font)
            
            # Save icons
            image.save('assets/app_icon.png')
            sizes = [48, 72, 96, 144, 192]
            for s in sizes:
                resized = image.resize((s, s), Image.LANCZOS)
                resized.save(f'assets/app_icon_{s}.png')

        def create_splash_screen(width=1080, height=1920):
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # Gradient background
            for y in range(height):
                r = int(50 + 205 * (y/height))
                g = int(50 + 150 * (y/height))
                b = int(50 + 100 * (y/height))
                for x in range(width):
                    draw.point((x, y), fill=(r, g, b))
            
            # Network icon
            icon_size = min(width, height) // 3
            draw.rectangle([
                (width - icon_size)//2, 
                (height - icon_size)//2, 
                (width + icon_size)//2, 
                (height + icon_size)//2
            ], outline='white', width=width//50)
            
            # Text
            try:
                font = ImageFont.truetype("arial.ttf", height//20)
            except IOError:
                font = ImageFont.load_default()
            
            draw.text(
                (width//4, height*3//4), 
                "IP FETCH\nNetwork Toolkit", 
                fill='white', 
                font=font
            )
            
            image.save('assets/splash_screen.png')

        create_app_icon()
        create_splash_screen()
        print("Assets created successfully in 'assets' directory.")

    except ImportError:
        print("Pillow library not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image, ImageDraw, ImageFont
        # Retry asset generation
        generate_assets()

def build_apk():
    """Build Android APK with comprehensive error handling"""
    print("\n🚀 Starting APK Build Process 🚀")
    
    # Detect platform and provide specific guidance
    if platform.system() == "Windows":
        print("⚠️ Windows APK Build Detected. Recommended to use WSL or Virtual Machine.")
        print("Alternative Options:")
        print("1. Use Windows Subsystem for Linux (WSL)")
        print("2. Use a Virtual Machine with Ubuntu")
        print("3. Use Cloud Build Services")
        
    try:
        # Verbose buildozer command
        command = [
            "buildozer", 
            "-v",  # Verbose mode
            "android", 
            "debug", 
            "deploy", 
            "run"
        ]
        
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        print("✅ APK Generated Successfully!")
        print("\n--- Build Output ---")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print("❌ APK Generation Failed:")
        print("\n--- STDOUT ---")
        print(e.stdout)
        print("\n--- STDERR ---")
        print(e.stderr)
        
        # Specific Windows Troubleshooting
        if platform.system() == "Windows":
            print("\n🔧 Windows Troubleshooting Tips:")
            print("1. Ensure Java Development Kit (JDK) is installed")
            print("2. Add Java and Android SDK to system PATH")
            print("3. Install Android SDK command-line tools")
            print("4. Consider using WSL or a Virtual Machine")
    
    except FileNotFoundError:
        print("❌ Buildozer not found. Please install:")
        print("pip install buildozer")

def main():
    print("🌐 Preparing IP FETCH Android APK 🌐")
    
    # System Requirements Check
    check_system_requirements()
    
    # Install Android Dependencies
    install_android_dependencies()
    
    # Generate Assets
    generate_assets()
    
    # Build APK
    build_apk()

if __name__ == "__main__":
    main()
