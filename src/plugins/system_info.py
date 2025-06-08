import platform
import psutil
from typing import Dict, Any

from core.plugin import Plugin, PluginCommand, PluginResponse

class SystemInfoPlugin(Plugin):
    """Plugin for retrieving system information."""
    
    def __init__(self):
        super().__init__("system_info")
    
    async def initialize(self) -> None:
        """Initialize the plugin."""
        await super().initialize()
    
    async def shutdown(self) -> None:
        """Shutdown the plugin."""
        await super().shutdown()
    
    async def handle_command(self, command: PluginCommand) -> PluginResponse:
        """Handle system information commands."""
        if command.command == "get_system_info":
            return await self._get_system_info()
        elif command.command == "get_cpu_info":
            return await self._get_cpu_info()
        elif command.command == "get_memory_info":
            return await self._get_memory_info()
        else:
            return PluginResponse(
                success=False,
                error=f"Unknown command: {command.command}"
            )
    
    async def _get_system_info(self) -> PluginResponse:
        """Get general system information."""
        try:
            info = {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            }
            return PluginResponse(success=True, data=info)
        except Exception as e:
            return PluginResponse(success=False, error=str(e))
    
    async def _get_cpu_info(self) -> PluginResponse:
        """Get CPU information."""
        try:
            info = {
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "cpu_freq": {
                    "current": psutil.cpu_freq().current,
                    "min": psutil.cpu_freq().min,
                    "max": psutil.cpu_freq().max
                }
            }
            return PluginResponse(success=True, data=info)
        except Exception as e:
            return PluginResponse(success=False, error=str(e))
    
    async def _get_memory_info(self) -> PluginResponse:
        """Get memory information."""
        try:
            memory = psutil.virtual_memory()
            info = {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
                "free": memory.free
            }
            return PluginResponse(success=True, data=info)
        except Exception as e:
            return PluginResponse(success=False, error=str(e)) 