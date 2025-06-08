#!/usr/bin/env python3
"""
MCP Application Installer
Creates a properly configured application bundle with pre-installed dependencies.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def create_installer():
    """Create the MCP application with all dependencies pre-installed."""
    
    print("🚀 Creating MCP Application Installer...")
    
    # Remove existing app if it exists
    if os.path.exists("MCP.app"):
        print("📁 Removing existing MCP.app...")
        shutil.rmtree("MCP.app")
    
    # Create app bundle structure
    app_path = Path("MCP.app")
    contents_path = app_path / "Contents"
    macos_path = contents_path / "MacOS"
    resources_path = contents_path / "Resources"
    
    print("📦 Creating app bundle structure...")
    macos_path.mkdir(parents=True, exist_ok=True)
    resources_path.mkdir(parents=True, exist_ok=True)
    
    # Create Info.plist
    info_plist = {
        'CFBundleName': 'MCP',
        'CFBundleDisplayName': 'MCP Control Panel',
        'CFBundleIdentifier': 'com.mcp.controlpanel',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': 'launcher',
        'CFBundleIconFile': 'MCP.icns',
        'LSApplicationCategoryType': 'public.app-category.developer-tools',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.14'
    }
    
    import plistlib
    with open(contents_path / "Info.plist", 'wb') as f:
        plistlib.dump(info_plist, f)
    
    # Copy icon if it exists
    if os.path.exists("MCP.icns"):
        print("🎨 Copying application icon...")
        shutil.copy2("MCP.icns", resources_path / "MCP.icns")
    
    # Create virtual environment
    print("🐍 Creating virtual environment...")
    venv_path = macos_path / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    
    # Install dependencies
    print("📦 Installing dependencies (this may take a moment)...")
    pip_path = venv_path / "bin" / "pip"
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    
    # Copy application files
    print("📄 Copying application files...")
    for item in ["src", "config", "launch.py"]:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.copytree(item, macos_path / item)
            else:
                shutil.copy2(item, macos_path / item)
    
    # Copy requirements.txt
    if os.path.exists("requirements.txt"):
        shutil.copy2("requirements.txt", macos_path / "requirements.txt")
    
    # Create optimized launcher script
    launcher_script = f'''#!/bin/bash

# MCP Application Launcher
cd "$(dirname "$0")"

# Clear previous logs
LOG_DIR="$HOME/Library/Logs/MCP"
if [ -d "$LOG_DIR" ]; then
    find "$LOG_DIR" -name "*.log" -mtime +7 -delete  # Keep logs for 7 days
fi

# Create log directory
mkdir -p "$LOG_DIR"

# Activate virtual environment
source ./venv/bin/activate

# Launch the application
exec python launch.py
'''
    
    launcher_path = macos_path / "launcher"
    with open(launcher_path, 'w') as f:
        f.write(launcher_script)
    
    # Make launcher executable
    os.chmod(launcher_path, 0o755)
    
    print("✅ MCP Application created successfully!")
    print(f"📱 You can now move MCP.app to your Applications folder")
    print(f"📊 Logs will be available at ~/Library/Logs/MCP/")
    print("🧹 Old logs will be automatically cleaned up after 7 days")

if __name__ == "__main__":
    create_installer() 