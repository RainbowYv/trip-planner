from ..config import get_settings

settings = get_settings()

mcp_config = {
        # --- 服务器 1: 高德地图 ---
        "amap-maps": {
            "command": "npx",
            "args": ["-y", "@amap/amap-maps-mcp-server"],
            "transport": "stdio",
            "env": {
                "AMAP_MAPS_API_KEY": settings.amap_api_key
            }
        },



    }
