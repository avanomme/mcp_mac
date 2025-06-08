from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 1024x1024 image with a dark background
    size = 1024
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a modern, minimalist design
    # Outer circle
    draw.ellipse([50, 50, size-50, size-50], fill='#2C3E50')
    
    # Inner circle
    draw.ellipse([150, 150, size-150, size-150], fill='#3498DB')
    
    # Center circle
    draw.ellipse([300, 300, size-300, size-300], fill='#ECF0F1')
    
    # Save the icon in different sizes
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    iconset_dir = "MCP.iconset"
    
    # Create iconset directory
    if not os.path.exists(iconset_dir):
        os.makedirs(iconset_dir)
    
    # Generate different sizes
    for s in sizes:
        resized = image.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f"{iconset_dir}/icon_{s}x{s}.png")
    
    print("Icon files created successfully!")
    print("To create .icns file, run the following command in terminal:")
    print("iconutil -c icns MCP.iconset")

if __name__ == "__main__":
    create_icon() 