from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool, BaseTool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from ..config import get_settings
from .LLMBase import get_llm, LLMBase


class AgentBase:
    def __init__(
            self,
            name: str,
            llm: Optional[ChatOpenAI] = None,
            model: Optional[str] = None,
            system_prompt: Optional[str] = None,
            tools: Optional[list[BaseTool]] = None,
    ):
        settings = get_settings()
        self.name = name
        self.llm = llm if llm is not None else get_llm(model=model)
        self.system_prompt = system_prompt
        self.tools = tools if tools is not None else []

    def run(
            self,
            input_text: str,
            **kwargs
    ) -> str:
        agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt,
        )
        messages = [HumanMessage(content=input_text)]
        response = agent.invoke({
            "messages": messages
        })
        return response["messages"][-1].content

    async def arun(
            self,
            input_text: str,
            **kwargs
    ) -> str:
        agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt,
        )
        messages = [HumanMessage(content=input_text)]
        response = await agent.ainvoke({
            "messages": messages
        })
        return response["messages"][-1].content

