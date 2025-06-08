import importlib
import inspect
from pathlib import Path
from typing import Dict, Type
from loguru import logger

from core.plugin import Plugin
from core.config import Settings

class PluginManager:
    """Manages the loading and lifecycle of plugins."""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.settings = Settings()
    
    async def initialize_plugins(self):
        """Initialize all enabled plugins."""
        plugins_dir = self.settings.plugins_dir
        
        if not plugins_dir.exists():
            logger.warning(f"Plugins directory {plugins_dir} does not exist")
            return
        
        # Load all Python files in the plugins directory
        for plugin_file in plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
                
            try:
                # Import the plugin module
                module_name = f"plugins.{plugin_file.stem}"
                module = importlib.import_module(module_name)
                
                # Find all Plugin subclasses in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Plugin) and 
                        obj != Plugin):
                        
                        # Initialize the plugin
                        plugin = obj()
                        plugin_name = plugin.name
                        
                        if plugin_name in self.plugins:
                            logger.warning(f"Plugin {plugin_name} already loaded, skipping")
                            continue
                            
                        if (not self.settings.enabled_plugins or 
                            plugin_name in self.settings.enabled_plugins):
                            await plugin.initialize()
                            self.plugins[plugin_name] = plugin
                            logger.info(f"Loaded plugin: {plugin_name}")
                
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_file.name}: {str(e)}")
    
    async def shutdown_plugins(self):
        """Shutdown all loaded plugins."""
        for plugin_name, plugin in self.plugins.items():
            try:
                await plugin.shutdown()
                logger.info(f"Shutdown plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error shutting down plugin {plugin_name}: {str(e)}")
        
        self.plugins.clear()
    
    def get_plugin(self, plugin_name: str) -> Plugin:
        """Get a plugin by name."""
        if plugin_name not in self.plugins:
            raise KeyError(f"Plugin {plugin_name} not found")
        return self.plugins[plugin_name]
    
    def list_plugins(self) -> Dict[str, Plugin]:
        """List all loaded plugins."""
        return self.plugins.copy() 