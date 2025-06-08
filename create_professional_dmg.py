#!/usr/bin/env python3
"""
MCP Professional macOS Installer Creator
Creates a beautiful .dmg installer with pre-installed dependencies.
"""

import os
import shutil
import subprocess
import sys
import json
from pathlib import Path

def create_background_image():
    """Create a modern background image for the DMG using Python."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a modern gradient background
        width, height = 600, 400
        img = Image.new('RGB', (width, height), '#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for y in range(height):
            color_value = int(240 - (y / height) * 20)
            color = (color_value, color_value, color_value + 10)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Add MCP branding
        try:
            # Try to use a nice font, fallback to default
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw title
        draw.text((50, 50), "MCP Control Panel", fill='#333333', font=font_large)
        draw.text((50, 110), "Master Control Program for macOS", fill='#666666', font=font_medium)
        
        # Draw installation instructions
        draw.text((50, 180), "Installation Instructions:", fill='#333333', font=font_medium)
        draw.text((50, 220), "1. Drag MCP.app to the Applications folder", fill='#555555', font=font_small)
        draw.text((50, 245), "2. Launch MCP from your Applications", fill='#555555', font=font_small)
        draw.text((50, 270), "3. Grant permissions when prompted", fill='#555555', font=font_small)
        
        # Draw arrow pointing to Applications
        arrow_points = [(450, 200), (500, 180), (500, 190), (580, 190), (580, 210), (500, 210), (500, 220)]
        draw.polygon(arrow_points, fill='#007AFF')
        
        # Save background
        img.save('dmg_background.png')
        return True
        
    except ImportError:
        print("PIL not available, creating simple background...")
        # Create a simple text file instead
        with open('dmg_background.txt', 'w') as f:
            f.write("Drag MCP.app to Applications folder to install")
        return False

def create_professional_dmg():
    """Create a professional DMG installer with pre-installed dependencies."""
    
    print("🚀 Creating MCP Professional Installer with Pre-installed Dependencies...")
    
    # Clean up any existing builds
    build_items = ["MCP.app", "MCP_Installer.dmg", "dmg_temp", "dist", "dmg_background.png"]
    for item in build_items:
        if os.path.exists(item):
            print(f"🧹 Cleaning up {item}...")
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
    
    # Create distribution directory
    dist_path = Path("dist")
    dist_path.mkdir(exist_ok=True)
    
    print("📦 Building MCP Application Bundle with Pre-installed Dependencies...")
    
    # Create app bundle structure
    app_path = dist_path / "MCP.app"
    contents_path = app_path / "Contents"
    macos_path = contents_path / "MacOS"
    resources_path = contents_path / "Resources"
    
    # Create directories
    macos_path.mkdir(parents=True, exist_ok=True)
    resources_path.mkdir(parents=True, exist_ok=True)
    
    # Create Info.plist
    info_plist = {
        'CFBundleName': 'MCP',
        'CFBundleDisplayName': 'MCP Control Panel',
        'CFBundleIdentifier': 'com.mcp.controlpanel',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': 'MCP',
        'CFBundleIconFile': 'MCP.icns',
        'LSApplicationCategoryType': 'public.app-category.developer-tools',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.14',
        'NSRequiresAquaSystemAppearance': False,
        'LSUIElement': False
    }
    
    import plistlib
    with open(contents_path / "Info.plist", 'wb') as f:
        plistlib.dump(info_plist, f)
    
    # Copy icon
    if os.path.exists("MCP.icns"):
        print("🎨 Adding application icon...")
        shutil.copy2("MCP.icns", resources_path / "MCP.icns")
    
    # Create virtual environment with pre-installed dependencies
    print("🐍 Creating virtual environment with pre-installed dependencies...")
    venv_path = macos_path / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    
    # Install dependencies into the virtual environment
    print("📦 Pre-installing all dependencies...")
    pip_path = venv_path / "bin" / "pip"
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
    
    if os.path.exists("requirements.txt"):
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    
    # Create the optimized main executable
    print("⚡ Creating optimized launcher...")
    
    main_executable = '''#!/usr/bin/env python3
"""
MCP Application Main Executable
Optimized launcher with pre-installed dependencies.
"""

import sys
import os
import subprocess
import time
import signal
import traceback
from pathlib import Path

def setup_environment():
    """Setup the application environment."""
    app_dir = Path(__file__).parent
    
    # Clear logs on every launch
    log_dir = Path.home() / "Library" / "Logs" / "MCP"
    if log_dir.exists():
        for log_file in log_dir.glob("*.log"):
            try:
                log_file.unlink()
            except:
                pass
    
    # Activate virtual environment
    venv_path = app_dir / "venv"
    if venv_path.exists():
        # Add venv to Python path
        venv_site_packages = venv_path / "lib"
        for python_dir in venv_site_packages.glob("python*"):
            site_packages = python_dir / "site-packages"
            if site_packages.exists():
                sys.path.insert(0, str(site_packages))
    
    # Add src to Python path
    src_dir = app_dir / "src"
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))
    
    # Change to app directory
    os.chdir(app_dir)
    
    return app_dir

def kill_existing_processes():
    """Kill any existing MCP processes."""
    try:
        result = subprocess.run(["lsof", "-ti:8080"], capture_output=True, text=True)
        if result.stdout:
            pids = result.stdout.strip().split('\\n')
            for pid in pids:
                if pid:
                    subprocess.run(["kill", "-9", pid], capture_output=True)
                    print(f"Killed existing process {pid} using port 8080")
    except:
        pass

def main():
    """Main application entry point."""
    try:
        print("🚀 Starting MCP Control Panel...")
        
        # Setup environment (clears logs and activates venv)
        app_dir = setup_environment()
        
        # Kill existing processes
        kill_existing_processes()
        
        # Import and run the application
        try:
            from utils.logger import logger
            logger.info("MCP Application starting with pre-installed dependencies...")
            
            # Import launch module
            import launch
            launch.main()
            
        except ImportError as e:
            print(f"Error importing application modules: {e}")
            print("Dependencies may not be properly installed.")
            return 1
            
    except KeyboardInterrupt:
        print("\\nApplication terminated by user.")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
    
    # Write the main executable
    main_exec_path = macos_path / "MCP"
    with open(main_exec_path, 'w') as f:
        f.write(main_executable)
    os.chmod(main_exec_path, 0o755)
    
    # Copy application files
    print("📄 Copying application files...")
    for item in ["src", "config"]:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, macos_path / item)
    
    # Copy launch.py
    if os.path.exists("launch.py"):
        shutil.copy2("launch.py", macos_path / "launch.py")
    
    # Copy requirements.txt for reference
    if os.path.exists("requirements.txt"):
        shutil.copy2("requirements.txt", macos_path / "requirements.txt")
    
    print("🎨 Creating modern DMG installer...")
    
    # Create background image
    has_background = create_background_image()
    
    # Create temporary DMG directory
    dmg_temp = Path("dmg_temp")
    dmg_temp.mkdir(exist_ok=True)
    
    # Copy app to DMG directory
    shutil.copytree(app_path, dmg_temp / "MCP.app")
    
    # Create Applications symlink
    applications_link = dmg_temp / "Applications"
    if applications_link.exists():
        applications_link.unlink()
    os.symlink("/Applications", applications_link)
    
    # Copy background image if created
    if has_background and os.path.exists('dmg_background.png'):
        shutil.copy2('dmg_background.png', dmg_temp / '.background.png')
    
    # Create modern README
    readme_content = """🚀 MCP Control Panel - Installation Guide

✨ QUICK INSTALL:
   Just drag MCP.app to the Applications folder!

📋 WHAT'S INCLUDED:
   ✅ Pre-installed Python dependencies
   ✅ FastAPI web server
   ✅ Modern web interface
   ✅ Automatic log management
   ✅ Professional macOS integration

🔧 SYSTEM REQUIREMENTS:
   • macOS 10.14 or later
   • No additional software needed!

🎯 FEATURES:
   • Lightning-fast startup (no dependency installation!)
   • Clean, modern interface
   • Automatic log cleanup
   • Professional macOS app bundle

🆘 TROUBLESHOOTING:
   If MCP doesn't start, check Console.app for errors
   or run: /Applications/MCP.app/Contents/MacOS/MCP

🗑️ TO UNINSTALL:
   Simply delete MCP.app from Applications

Enjoy your MCP Control Panel! 🎊
"""
    
    with open(dmg_temp / "📖 Read Me.txt", 'w') as f:
        f.write(readme_content)
    
    # Create the DMG
    dmg_name = "MCP_Professional_Installer.dmg"
    print(f"🗜️  Creating {dmg_name}...")
    
    # Remove existing DMG
    if os.path.exists(dmg_name):
        os.remove(dmg_name)
    
    # Create DMG using hdiutil with modern styling
    create_dmg_cmd = [
        "hdiutil", "create",
        "-srcfolder", str(dmg_temp),
        "-volname", "MCP Control Panel",
        "-fs", "HFS+",
        "-fsargs", "-c c=64,a=16,e=16",
        "-format", "UDBZ",
        "-imagekey", "zlib-level=9",
        dmg_name
    ]
    
    result = subprocess.run(create_dmg_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        file_size = os.path.getsize(dmg_name) / (1024*1024)
        print(f"✅ Successfully created {dmg_name}")
        print(f"📦 DMG size: {file_size:.1f} MB")
        print(f"🎯 Professional installer ready for distribution!")
        print(f"")
        print(f"🌟 KEY IMPROVEMENTS:")
        print(f"   ✅ All dependencies pre-installed")
        print(f"   ✅ Lightning-fast app startup")
        print(f"   ✅ Logs cleared on every launch")
        print(f"   ✅ Modern DMG design")
        print(f"   ✅ Professional user experience")
        print(f"")
        print(f"📱 DISTRIBUTION READY:")
        print(f"   Users simply download → mount → drag to Applications → launch!")
    else:
        print(f"❌ Error creating DMG: {result.stderr}")
        return False
    
    # Cleanup
    shutil.rmtree(dmg_temp)
    shutil.rmtree(dist_path)
    if os.path.exists('dmg_background.png'):
        os.remove('dmg_background.png')
    
    return True

if __name__ == "__main__":
    if not create_professional_dmg():
        sys.exit(1)
    print("🎊 MCP Professional Installer creation completed successfully!") 