import os
from typing import Optional

from langchain_openai import ChatOpenAI

from ..config import get_settings

_llm_instance = None


class LLMBase:
    def __init__(
            self,
            model: Optional[str] = None,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: Optional[int] = None,
            timeout: Optional[int] = None,
            **kwargs
    ):
        self.model = model or os.getenv("LLM_MODEL_ID")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT", "60"))
        self.kwargs = kwargs
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        self.client = self._create_client()

    def _create_client(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
        )


def get_llm(model: str = None) -> ChatOpenAI:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLMBase(model=model)

        print(f"✅ LLM服务初始化成功")
        print(f"   模型: {_llm_instance.model}")

    return _llm_instance.client


def reset_llm():
    """重置LLM实例(用于测试或重新配置)"""
    global _llm_instance
    _llm_instance = None
