from pydantic import BaseSettings, Field
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""
    
    # Server settings
    host: str = Field(default="localhost", env="MCP_HOST")
    port: int = Field(default=8080, env="MCP_PORT")
    
    # Security settings
    secret_key: str = Field(default="your-secret-key-here", env="MCP_SECRET_KEY")
    token_expire_minutes: int = Field(default=30, env="MCP_TOKEN_EXPIRE_MINUTES")
    
    # Plugin settings
    plugins_dir: Path = Field(default=Path("plugins"), env="MCP_PLUGINS_DIR")
    enabled_plugins: List[str] = Field(default_factory=list)
    
    # Logging settings
    log_level: str = Field(default="INFO", env="MCP_LOG_LEVEL")
    log_file: Optional[Path] = Field(default=None, env="MCP_LOG_FILE")
    
    # API settings
    api_prefix: str = Field(default="/api", env="MCP_API_PREFIX")
    rate_limit: int = Field(default=100, env="MCP_RATE_LIMIT")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Ensure plugins directory exists
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True) 