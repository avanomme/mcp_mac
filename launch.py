import webview
import subprocess
import time
import sys
import os
import signal
import traceback
from pathlib import Path

# Add src to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(src_path)

from utils.logger import logger

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_fastapi_server():
    try:
        # Path to your FastAPI app
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fastapi_script = os.path.join(script_dir, 'src', 'main.py')
        
        logger.info(f"Looking for FastAPI script at: {fastapi_script}")
        
        if not os.path.exists(fastapi_script):
            logger.error(f"FastAPI script not found at {fastapi_script}")
            return None
        
        # Check if port is already in use
        if is_port_in_use(8080):
            logger.warning("Port 8080 is already in use. The server might already be running.")
            return None
        
        # Start FastAPI server as a subprocess
        logger.info("Starting FastAPI server...")
        fastapi_proc = subprocess.Popen(
            [sys.executable, fastapi_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Simple wait for the server to start
        logger.info('Waiting for FastAPI server to start...')
        time.sleep(3)  # Give the server time to start
        
        # Check if process is still running
        if fastapi_proc.poll() is not None:
            stdout, stderr = fastapi_proc.communicate()
            logger.error(f"FastAPI server failed to start. Error: {stderr}")
            return None
        
        logger.info("FastAPI server started successfully")
        return fastapi_proc
    except Exception as e:
        logger.error(f"Error starting FastAPI server: {str(e)}")
        logger.error(traceback.format_exc())
        return None

def main():
    try:
        logger.info("Starting MCP application...")
        
        # Start the FastAPI server
        fastapi_proc = start_fastapi_server()
        if not fastapi_proc:
            logger.error("Failed to start FastAPI server")
            return
        
        # Create and start the webview window
        try:
            logger.info("Creating webview window...")
            window = webview.create_window(
                'MCP Control Panel',
                'http://localhost:8080/docs',
                width=1200,
                height=800,
                resizable=True,
                min_size=(800, 600)
            )
            logger.info("Starting webview...")
            webview.start(debug=True)
        except Exception as e:
            logger.error(f"Error creating webview window: {str(e)}")
            logger.error(traceback.format_exc())
        finally:
            # Cleanup when the window is closed
            if fastapi_proc:
                logger.info("Shutting down FastAPI server...")
                fastapi_proc.terminate()
                fastapi_proc.wait()
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        if 'fastapi_proc' in locals() and fastapi_proc:
            fastapi_proc.terminate()
            fastapi_proc.wait()
    
    logger.info("MCP application shutdown complete")

if __name__ == "__main__":
    main() 