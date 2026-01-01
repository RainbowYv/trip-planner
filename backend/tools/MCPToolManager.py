from typing import Optional, List
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from .mcp_config import mcp_config


class MCPToolManager:
    _instance = None
    _client = None
    _tools: List[BaseTool] = []
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MCPToolManager, cls).__new__(cls)
        return cls._instance

    async def initialize(self, config: Optional[dict] = None):
        """
        [异步] 初始化连接并加载工具。
        """
        if self._is_initialized:
            return

        print("--- [MCP Manager] 正在初始化连接... ---")
        if config is None:
            config = mcp_config

        # 1. 初始化客户端 (这是一个长生命周期的对象)
        self._client = MultiServerMCPClient(config)

        try:
            self._tools = await self._client.get_tools()

            print(f"--- [MCP Manager] 成功加载 {len(self._tools)} 个工具 ---")
            for t in self._tools:
                print(f"  - 工具：{t.name} ,功能描述：{t.description}")

            self._is_initialized = True
        except Exception as e:
            print(f"--- [MCP Manager] 初始化失败: {e} ---")
            # 出错时重置
            self._client = None
            raise e

    def get_tools(self) -> List[BaseTool]:
        """
        [同步] 获取缓存的工具列表。
        """
        if not self._is_initialized:
            print("⚠️ [MCP Manager] 尚未初始化，返回空列表")
            return []
        return self._tools

    async def close(self):
        """清理资源"""
        if self._client:
            print("--- [MCP Manager] 释放客户端引用 ---")
            self._client = None
            self._is_initialized = False
