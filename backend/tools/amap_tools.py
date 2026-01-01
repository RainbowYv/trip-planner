"""高德地图MCP服务封装"""
from .MCPToolManager import MCPToolManager
from .mcp_config import mcp_config

_amap_mcp_tool = None


async def get_amap_mcp_tool():
    global _amap_mcp_tool
    if _amap_mcp_tool is not None:
        return _amap_mcp_tool

    mcp_tool_manager = MCPToolManager()
    config = {"amap-maps": mcp_config["amap-maps"]}
    await mcp_tool_manager.initialize(config)

    _amap_mcp_tool = mcp_tool_manager.get_tools()
    return _amap_mcp_tool
