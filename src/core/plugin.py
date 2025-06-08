from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class PluginCommand(BaseModel):
    """Base model for plugin commands."""
    command: str
    parameters: Dict[str, Any] = {}

class PluginResponse(BaseModel):
    """Base model for plugin responses."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class Plugin(ABC):
    """Base class for all MCP plugins."""
    
    def __init__(self, name: str):
        self.name = name
        self._initialized = False
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the plugin.
        
        This method should be implemented by all plugins to perform any necessary
        setup, such as connecting to external services or initializing resources.
        """
        self._initialized = True
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Shutdown the plugin.
        
        This method should be implemented by all plugins to perform any necessary
        cleanup, such as closing connections or releasing resources.
        """
        self._initialized = False
    
    @abstractmethod
    async def handle_command(self, command: PluginCommand) -> PluginResponse:
        """Handle a command sent to the plugin.
        
        Args:
            command: The command to handle
            
        Returns:
            A PluginResponse object containing the result of the command
        """
        if not self._initialized:
            return PluginResponse(
                success=False,
                error="Plugin not initialized"
            )
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the plugin.
        
        Returns:
            A dictionary containing plugin information
        """
        return {
            "name": self.name,
            "initialized": self._initialized
        }
    
    def is_initialized(self) -> bool:
        """Check if the plugin is initialized.
        
        Returns:
            True if the plugin is initialized, False otherwise
        """
        return self._initialized 