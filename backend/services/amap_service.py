"""高德地图MCP服务封装"""
import json
from typing import List, Dict, Any, Optional
from ..config import get_settings
from ..models.schemas import Location, POIInfo, WeatherInfo
from ..tools.amap_tools import get_amap_mcp_tool

# 全局MCP工具实例
_amap_mcp_tool = None


class AmapService:
    """高德地图服务封装类 (Async)"""

    def __init__(self):
        """
        初始化服务
        注意: 这里只做基本状态初始化，工具加载放在 initialize 中
        """
        self.tools_map = {}
        self._is_initialized = False

    async def initialize(self):
        """[异步] 初始化：获取 MCP 工具并建立映射"""
        if self._is_initialized:
            return

        print("🔄 [AmapService] 正在初始化工具...")
        try:
            # 1. 获取工具列表 (这会等待 MCP 连接建立)
            tools_list = await get_amap_mcp_tool()

            # 2. 建立 工具名 -> 工具对象 的映射，方便查找
            # 假设工具名可能是 'amap_maps_text_search'，我们存储完整名字
            self.tools_map = {t.name: t for t in tools_list}

            print(f"✅ [AmapService] 加载了 {len(self.tools_map)} 个工具: {list(self.tools_map.keys())}")
            self._is_initialized = True
        except Exception as e:
            print(f"❌ [AmapService] 初始化失败: {e}")
            raise e

    async def _call_tool(self, partial_name: str, arguments: Dict[str, Any]) -> str:
        """
        [内部助手] 查找并调用工具
        Args:
            partial_name: 工具名关键字 (如 'maps_text_search')
            arguments: 参数字典
        """
        if not self._is_initialized:
            await self.initialize()

        # 1. 查找工具 (支持模糊匹配，防止前缀变化)
        # 例如找 "maps_text_search"，能匹配到 "amap_maps_text_search"
        target_tool = next(
            (tool for name, tool in self.tools_map.items() if partial_name in name),
            None
        )

        if not target_tool:
            raise ValueError(f"未找到名称包含 '{partial_name}' 的 MCP 工具")

        # 2. 异步调用
        # print(f"🔌 调用工具 [{target_tool.name}] 参数: {arguments}")
        result = await target_tool.ainvoke(arguments)
        return result

    async def search_poi(self, keywords: str, city: str, citylimit: bool = True) -> List[POIInfo]:
        """[异步] 搜索POI"""
        try:
            # 调用工具
            response_str = await self._call_tool(
                "maps_text_search",
                {
                    "keywords": keywords,
                    "city": city,
                    "citylimit": str(citylimit).lower()
                }
            )

            # 解析结果 (假设返回的是 JSON 字符串)
            # 注意：实际 MCP 返回的可能是纯文本或 JSON，需要根据你的 Server 实现来调整解析逻辑
            data = self._parse_json(response_str)

            # TODO: 这里需要根据高德 API 实际返回结构转为 POIInfo 对象
            # 示例仅返回原始数据用于调试
            # pois = [POIInfo(**item) for item in data.get('pois', [])]
            print(f"POI搜索结果(片段): {str(data)[:100]}...")
            return []

        except Exception as e:
            print(f"❌ POI搜索失败: {str(e)}")
            return []

    async def get_weather(self, city: str) -> List[WeatherInfo]:
        """[异步] 查询天气"""
        try:
            response_str = await self._call_tool(
                "maps_weather",
                {"city": city}
            )

            data = self._parse_json(response_str)
            print(f"天气查询结果: {str(data)[:100]}...")
            return []

        except Exception as e:
            print(f"❌ 天气查询失败: {str(e)}")
            return []

    async def plan_route(
            self,
            origin_address: str,
            destination_address: str,
            origin_city: Optional[str] = None,
            destination_city: Optional[str] = None,
            route_type: str = "walking"
    ) -> Dict[str, Any]:
        """[异步] 规划路线"""
        try:
            tool_map = {
                "walking": "maps_direction_walking_by_address",
                "driving": "maps_direction_driving_by_address",
                "transit": "maps_direction_transit_integrated_by_address"
            }
            tool_suffix = tool_map.get(route_type, "maps_direction_walking_by_address")

            arguments = {
                "origin_address": origin_address,
                "destination_address": destination_address
            }
            if origin_city: arguments["origin_city"] = origin_city
            if destination_city: arguments["destination_city"] = destination_city

            response_str = await self._call_tool(tool_suffix, arguments)
            return self._parse_json(response_str)

        except Exception as e:
            print(f"❌ 路线规划失败: {str(e)}")
            return {}

    async def geocode(self, address: str, city: Optional[str] = None) -> Optional[Location]:
        """[异步] 地理编码"""
        try:
            arguments = {"address": address}
            if city: arguments["city"] = city

            response_str = await self._call_tool("maps_geo", arguments)
            data = self._parse_json(response_str)
            print(f"地理编码结果: {str(data)[:100]}...")
            return None

        except Exception as e:
            print(f"❌ 地理编码失败: {str(e)}")
            return None

    async def get_poi_detail(self, poi_id: str) -> Dict[str, Any]:
        """[异步] 获取POI详情"""
        try:
            response_str = await self._call_tool("maps_search_detail", {"id": poi_id})
            return self._parse_json(response_str)
        except Exception as e:
            print(f"❌ 获取POI详情失败: {str(e)}")
            return {}

    def _parse_json(self, content: str) -> Any:
        """尝试解析 JSON 字符串"""
        if isinstance(content, (dict, list)):
            return content
        try:
            # 清理可能的 Markdown 代码块
            cleaned = content.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return content


# 创建全局服务实例
_amap_service = None


def get_amap_service() -> AmapService:
    """获取高德地图服务实例(单例模式)"""
    global _amap_service

    if _amap_service is None:
        _amap_service = AmapService()

    return _amap_service
