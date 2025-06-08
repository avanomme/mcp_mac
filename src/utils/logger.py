import logging
import os
import sys
from pathlib import Path
from datetime import datetime

def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = Path.home() / "Library" / "Logs" / "MCP"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"mcp_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG to capture everything
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create a logger for this module
    logger = logging.getLogger('MCP')
    
    # Log system information
    logger.info("=== MCP Application Start ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Platform: {sys.platform}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Log file: {log_file}")
    
    return logger

# Create a global logger instance
logger = setup_logging() 