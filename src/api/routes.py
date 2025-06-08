from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from loguru import logger

from core.plugin_manager import PluginManager
from core.plugin import PluginCommand, PluginResponse

router = APIRouter()

# Dependency to get plugin manager
def get_plugin_manager() -> PluginManager:
    from main import plugin_manager
    return plugin_manager

@router.get("/plugins")
async def list_plugins(
    plugin_manager: PluginManager = Depends(get_plugin_manager)
) -> Dict[str, Dict]:
    """List all loaded plugins and their status."""
    plugins = plugin_manager.list_plugins()
    return {
        name: plugin.get_info()
        for name, plugin in plugins.items()
    }

@router.get("/plugins/{plugin_name}")
async def get_plugin_info(
    plugin_name: str,
    plugin_manager: PluginManager = Depends(get_plugin_manager)
) -> Dict:
    """Get information about a specific plugin."""
    try:
        plugin = plugin_manager.get_plugin(plugin_name)
        return plugin.get_info()
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Plugin {plugin_name} not found"
        )

@router.post("/plugins/{plugin_name}/command")
async def execute_plugin_command(
    plugin_name: str,
    command: PluginCommand,
    plugin_manager: PluginManager = Depends(get_plugin_manager)
) -> PluginResponse:
    """Execute a command on a specific plugin."""
    try:
        plugin = plugin_manager.get_plugin(plugin_name)
        if not plugin.is_initialized():
            raise HTTPException(
                status_code=400,
                detail=f"Plugin {plugin_name} is not initialized"
            )
        
        response = await plugin.handle_command(command)
        return response
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Plugin {plugin_name} not found"
        )
    except Exception as e:
        logger.error(f"Error executing command on plugin {plugin_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error executing command: {str(e)}"
        ) 