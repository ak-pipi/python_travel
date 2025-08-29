# -*- encoding:utf-8 -*-
"""
    @project: Langchain_agent
    @Author：piyj
    @file： travel_agent.py
    @time：2025/8/26 14:21
"""

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from typing import Dict, Any
from utils.tavily_tools import tavily_searcher
from utils.deepseek_client import deepseek_client



class TavilyTravelAgent:
    def __init__(self):
        self.llm = deepseek_client.llm
        self.tavily_key = tavily_searcher.tavily_api_key
        self.tools = self._create_tools()
        self.agent = self._create_agent()

    def _create_tools(self) -> list:
        """创建工具列表"""
        return [tavily_searcher.search_tool]

    def _create_agent(self) -> Any:
        """创建Tavily增强的Agent"""
        try:
            agent = initialize_agent(
                tools=self.tools,
                llm=self.llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,
                return_intermediate_steps=False
            )
            return agent
        except Exception as e:
            print(f"创建Agent失败: {e}")
            return None

    def generate_travel_plan(self, summary: str) -> Dict[str, Any]:
        """使用Tavily生成旅行攻略"""
        if self.agent is None:
            return self._generate_without_agent(summary)

        try:
            query = f"""
作为专业旅行规划师，请根据以下用户需求生成详细的旅行攻略：

用户需求：{summary}

请使用Tavily搜索最新信息并生成包含以下内容的攻略：
1. 📅 每日具体行程（精确到早中晚时间段）
2. 🚗 交通方式建议（具体班次、价格估算）
3. 🏨 住宿推荐（具体酒店名称、价格范围）
4. 🏞️ 景区推荐和详细介绍（开放时间、门票价格）
5. 🍽️ 餐饮建议（推荐餐厅、特色美食）
6. 💰 预算分配建议
7. ⚠️ 注意事项和实用贴士

请确保信息准确、最新，并且基于2025年的实际情况。
"""

            result = self.agent.run(query)

            return {
                "status": "success",
                "plan_text": result,
                "word_count": len(result),
                "search_used": True,
                "search_engine": "tavily"
            }

        except Exception as e:
            print(f"Tavily Agent执行失败: {e}")
            return self._generate_without_agent(summary)

    def _generate_without_agent(self, summary: str) -> Dict[str, Any]:
        """不使用Agent的直接生成"""
        from langchain.prompts import ChatPromptTemplate
        from langchain.schema.output_parser import StrOutputParser

        try:
            prompt = ChatPromptTemplate.from_template("""
作为专业旅行规划师，请基于最新旅行信息为以下需求生成详细攻略：

{summary}

请提供包含以下内容的详细攻略：
- 每日具体时间安排（早中晚）
- 交通和住宿具体建议
- 景点详细介绍和门票信息
- 餐饮推荐和预算估算
- 实用注意事项

请确保信息准确实用。
""")

            chain = prompt | self.llm | StrOutputParser()
            result = chain.invoke({"summary": summary})

            return {
                "status": "success",
                "plan_text": result,
                "word_count": len(result),
                "search_used": False,
                "search_engine": "none"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "plan_text": ""
            }


# 单例实例
tavily_agent = TavilyTravelAgent()


# def get_tavily_agent(llm, api_key: str = None):
#     """获取Tavily Agent单例"""
#     global tavily_agent
#     if tavily_agent is None:
#         tavily_agent = TavilyTravelAgent(llm, api_key)
#     return tavily_agent