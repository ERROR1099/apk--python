from PIL import Image, ImageDraw, ImageFont
import os

# Create assets directory
os.makedirs('assets', exist_ok=True)

# Create App Icon
def create_app_icon(size=512):
    # Create a new image with a gradient background
    image = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(image)
    
    # Create a gradient background
    for y in range(size):
        r = int(255 * (1 - y/size))
        g = int(200 * (1 - y/size))
        b = int(100 * (1 - y/size))
        for x in range(size):
            draw.point((x, y), fill=(r, g, b))
    
    # Draw network-related icon elements
    draw.rectangle([size//4, size//4, size*3//4, size*3//4], 
                   outline='white', width=size//20)
    draw.line([size//3, size//2, size*2//3, size//2], 
              fill='white', width=size//30)
    draw.line([size//2, size//3, size//2, size*2//3], 
              fill='white', width=size//30)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", size//10)
    except IOError:
        font = ImageFont.load_default()
    
    draw.text((size//4, size*7//8), "IP FETCH", 
              fill='white', font=font)
    
    # Save the icon
    image.save('assets/app_icon.png')
    
    # Create multiple sizes for different device densities
    sizes = [48, 72, 96, 144, 192]
    for s in sizes:
        resized = image.resize((s, s), Image.LANCZOS)
        resized.save(f'assets/app_icon_{s}.png')

# Create Splash Screen
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
    
    # Draw network icon
    icon_size = min(width, height) // 3
    draw.rectangle([
        (width - icon_size)//2, 
        (height - icon_size)//2, 
        (width + icon_size)//2, 
        (height + icon_size)//2
    ], outline='white', width=width//50)
    
    # Add text
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
    
    # Save splash screen
    image.save('assets/splash_screen.png')

# Generate assets
if __name__ == "__main__":
    create_app_icon()
    create_splash_screen()
    print("Assets created successfully in 'assets' directory.")
