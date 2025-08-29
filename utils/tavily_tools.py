# -*- encoding:utf-8 -*-
"""
    @project: Langchain_agent
    @Author：piyj
    @file： tavily_tools.py
    @time：2025/8/28 17:14
"""

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import Tool
from typing import Dict, Any, List
from conf.tavily_conf_manager import config_more_manager

class TavilySearch:
    """Tavily搜索工具封装"""

    def __init__(self, tavily_key: str = None):

        # 获取tavilyKey
        config_more = config_more_manager.get_tavily_config()
        self.tavily_api_key = tavily_key or config_more.get('tavily_key')
        self.search_tool = self._create_search_tool()

    def _create_search_tool(self) -> Tool:
        """创建Tavily搜索工具"""
        try:
            search = TavilySearchResults(
                tavily_api_key=self.tavily_api_key,
                max_results=3,  # 每次搜索返回的最大结果数
                search_depth="advanced",  # 搜索深度：basic or advanced
                include_answer=True,  # 是否包含直接答案
                include_images=False,  # 是否包含图片
                include_raw_content=False  # 是否包含原始内容
            )

            return Tool(
                name="tavily_search",
                func=search.run,
                description="""专业的旅行信息搜索引擎。用于搜索：
- 最新的旅行攻略和指南
- 景点开放时间和门票价格
- 酒店和住宿信息
- 交通方式和价格
- 当地美食推荐
- 旅行注意事项和贴士
输入应该是具体的搜索查询。"""
            )

        except Exception as e:
            print(self.tavily_api_key)
            print(f"创建Tavily搜索工具失败: {e}")
            return self._create_fallback_tool()

    def _create_fallback_tool(self) -> Tool:
        """创建备用搜索工具"""
        try:
            from langchain_community.tools import DuckDuckGoSearchRun
            search = DuckDuckGoSearchRun()
            return Tool(
                name="web_search",
                func=search.run,
                description="通用网络搜索引擎"
            )
        except:
            # 如果所有搜索工具都不可用
            return Tool(
                name="no_search",
                func=lambda x: "搜索服务暂时不可用",
                description="搜索功能不可用"
            )

    def search_travel_info(self, query: str, max_results: int = 3) -> List[Dict]:
        """搜索旅行信息"""
        try:
            results = self.search_tool.run(f"{query} 2024 最新")
            return self._parse_search_results(results, max_results)
        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def _parse_search_results(self, results: Any, max_results: int) -> List[Dict]:
        """解析搜索结果"""
        parsed_results = []

        try:
            if isinstance(results, list):
                for result in results[:max_results]:
                    parsed_results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", "")[:200] + "...",
                        "score": result.get("score", 0)
                    })
            elif isinstance(results, str):
                # 如果是字符串结果，直接返回
                parsed_results.append({
                    "title": "搜索结果",
                    "content": results[:500] + "..." if len(results) > 500 else results
                })

        except Exception as e:
            print(f"解析搜索结果失败: {e}")

        return parsed_results


# 创建单例实例
tavily_searcher = TavilySearch()

# def get_tavily_searcher(tavily_key: str = None):
#     """获取Tavily搜索器单例"""
#     global tavily_searcher
#     if tavily_searcher is None:
#         tavily_searcher = TavilySearch(tavily_key)
#     return tavily_searcher