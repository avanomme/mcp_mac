import os
import shutil
import plistlib
from pathlib import Path

def create_app_bundle():
    # App bundle structure
    app_name = "MCP.app"
    contents_dir = os.path.join(app_name, "Contents")
    macos_dir = os.path.join(contents_dir, "MacOS")
    resources_dir = os.path.join(contents_dir, "Resources")
    
    # Create directory structure
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)
    
    # Create Info.plist
    info_plist = {
        "CFBundleName": "MCP",
        "CFBundleDisplayName": "MCP Control Panel",
        "CFBundleIdentifier": "com.mcp.controlpanel",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundlePackageType": "APPL",
        "CFBundleSignature": "????",
        "LSMinimumSystemVersion": "10.13.0",
        "CFBundleIconFile": "MCP.icns",
        "NSHighResolutionCapable": True,
        "LSApplicationCategoryType": "public.app-category.utilities",
    }
    
    with open(os.path.join(contents_dir, "Info.plist"), "wb") as f:
        plistlib.dump(info_plist, f)
    
    # Copy icon
    shutil.copy("MCP.icns", resources_dir)
    
    # Create launcher script with better error handling and logging
    launcher_script = """#!/bin/bash

# Set up logging
LOG_DIR="$HOME/Library/Logs/MCP"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/mcp_launcher.log"
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$LOG_FILE" >&2)

echo "Starting MCP application..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "Installing/updating requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Start the application
echo "Launching MCP..."
python launch.py

# If we get here, the application has exited
echo "MCP application exited"
"""
    
    with open(os.path.join(macos_dir, "MCP"), "w") as f:
        f.write(launcher_script)
    
    # Make launcher executable
    os.chmod(os.path.join(macos_dir, "MCP"), 0o755)
    
    # Copy application files
    print("Copying application files...")
    shutil.copytree("src", os.path.join(macos_dir, "src"), dirs_exist_ok=True)
    shutil.copytree("config", os.path.join(macos_dir, "config"), dirs_exist_ok=True)
    shutil.copy("launch.py", macos_dir)
    shutil.copy("requirements.txt", macos_dir)
    
    print(f"Application bundle created at {app_name}")
    print("You can now move MCP.app to your Applications folder")
    print("Logs will be available at ~/Library/Logs/MCP/")

if __name__ == "__main__":
    create_app_bundle() 