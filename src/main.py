import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import yaml
import os
from pathlib import Path

from core.plugin_manager import PluginManager
from core.config import Settings
from api.routes import router as api_router

# Initialize FastAPI app
app = FastAPI(
    title="MCP Server",
    description="Master Control Program Server for macOS",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load configuration
def load_config():
    config_path = Path("config/config.yaml")
    if not config_path.exists():
        logger.warning("Config file not found, using default settings")
        return Settings()
    
    with open(config_path) as f:
        config_data = yaml.safe_load(f)
    return Settings(**config_data)

# Initialize plugin manager
plugin_manager = PluginManager()

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    try:
        # Load configuration
        settings = load_config()
        
        # Initialize plugins
        await plugin_manager.initialize_plugins()
        
        logger.info("MCP Server started successfully")
    except Exception as e:
        logger.error(f"Failed to start MCP Server: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    try:
        await plugin_manager.shutdown_plugins()
        logger.info("MCP Server shut down successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

# Include API routes
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8080,
        reload=True,
        log_level="info"
    ) 