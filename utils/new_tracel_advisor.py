# -*- encoding:utf-8 -*-
"""
    @project: Langchain_agent
    @Author：piyj
    @file： new_tracel_advisor.py
    @time：2025/8/27 14:27
"""

from datetime import datetime
from typing import Dict, List, Any
from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory

from utils.deepseek_client import deepseek_client
from utils.summary_generator import summary_generator
# from utils.travel_plan_generator import plan_generator


class TravelAdvisor:
    def __init__(self, storage_type: str = "in_memory"):
        """
        初始化旅行顾问

        Args:
            storage_type: 存储类型 ("in_memory", "sqlite", "redis")
        """
        self.storage_type = storage_type
        self.conversation_histories: Dict[str, BaseChatMessageHistory] = {}

    def _get_chat_history(self, user_id: str) -> BaseChatMessageHistory:
        """获取或创建聊天历史"""
        if not user_id:
            user_id = "anonymous"

        if user_id not in self.conversation_histories:
            self.conversation_histories[user_id] = ChatMessageHistory()

        return self.conversation_histories[user_id]

    def process_user_input(self, user_input: str, user_id: str = None) -> dict:
        """处理用户输入并返回问题"""
        try:
            # 保存对话历史
            self._add_to_history(user_id, "user", user_input)

            # 生成挖掘问题
            questions = deepseek_client.generate_questions(user_input)
            # 保存生成的问题
            self._add_to_history(user_id, "assistant", {
                "type": "questions",
                "data": questions,
                "timestamp": datetime.now().isoformat()
            })

            return {
                "status": "success",
                "type": "questions",
                "questions": questions,
                "message": "请回答以下问题以帮助我们更好地了解您的需求"
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": f"处理请求时出错: {str(e)}"
            }

    def process_answers(self, answers: dict, user_id: str = None) -> dict:
        """处理用户答案并可能生成更多问题或推荐"""
        try:
            # 保存用户答案
            self._add_to_history(user_id, "user", {
                "type": "answers",
                "data": answers,
                "timestamp": datetime.now().isoformat()
            })

            return {
                "status": "success",
                "type": "recommendation",
                "message": "感谢您的回答！基于您的需求，我们正在生成旅行建议...",
                "next_step": "generate_recommendation"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"处理答案时出错: {str(e)}"
            }

    def generate_travel_summary(self, user_id: str, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成旅行需求总结
        """
        try:
            # 获取用户历史记录
            history = self.get_history(user_id)
            if not history:
                return {
                    "status": "error",
                    "message": "找不到用户对话历史"
                }

            # 查找用户初始需求
            user_input = ""
            for entry in history:
                if entry["role"] == "user" and isinstance(entry["content"], str):
                    user_input = entry["content"]
                    break

            if not user_input:
                user_input = "旅行需求"

            # 生成总结
            result = summary_generator.generate_travel_summary(user_input, answers)

            # 保存总结到历史
            if result["status"] == "success":
                self._add_to_history(user_id, "assistant", {
                    "type": "summary",
                    "data": result["summary"],
                    "key_points": result.get("key_points", {}),
                    "timestamp": datetime.now().isoformat()
                })

            return result

        except Exception as e:
            print(f"❌ 生成旅行总结时出错: {e}")
            return {
                "status": "error",
                "message": f"生成总结时出错: {str(e)}"
            }

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户对话历史（格式化）"""
        if not user_id:
            user_id = "anonymous"

        if user_id not in self.conversation_histories:
            return []

        chat_history = self.conversation_histories[user_id]
        formatted_history = []

        for message in chat_history.messages:
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            elif isinstance(message, SystemMessage):
                role = "system"
            else:
                role = "unknown"

            formatted_history.append({
                "role": role,
                "content": message.content,
                "type": message.type,
                "timestamp": datetime.now().isoformat()  # LangChain消息没有内置时间戳
            })

        return formatted_history

    def get_langchain_messages(self, user_id: str) -> List:
        """获取原始的LangChain消息对象"""
        if not user_id:
            user_id = "anonymous"

        if user_id not in self.conversation_histories:
            return []

        return self.conversation_histories[user_id].messages

    # def generate_travel_plan(self, user_id: str) -> Dict[str, Any]:
    #     """
    #     为用户生成旅行攻略
    #     """
    #     try:
    #         # 获取用户最新的需求总结
    #         summary = self._get_latest_summary(user_id)
    #         if not summary:
    #             return {
    #                 "status": "error",
    #                 "message": "未找到用户的需求总结，请先完成需求分析"
    #             }
    #
    #         print(f"📋 为用户 {user_id} 生成攻略，基于总结: {summary[:100]}...")
    #
    #         # 生成详细攻略
    #         result = plan_generator.generate_detailed_plan(summary)
    #
    #         # 保存攻略到历史
    #         if result["status"] == "success":
    #             self._add_to_history(user_id, "assistant", {
    #                 "type": "travel_plan",
    #                 "data": result["plan_text"],
    #                 "structured_data": result.get("structured_plan", {}),
    #                 "quality_score": result.get("quality_score", 0),
    #                 "timestamp": datetime.now().isoformat()
    #             })
    #
    #         return result
    #
    #     except Exception as e:
    #         print(f"❌ 生成旅行攻略时出错: {e}")
    #         return {
    #             "status": "error",
    #             "message": f"生成攻略时出错: {str(e)}"
    #         }

    def _get_latest_summary(self, user_id: str) -> str:
        """获取用户最新的需求总结"""
        if not user_id:
            user_id = "anonymous"

        if user_id not in self.conversation_histories:
            return ""

        # 从最新到最旧遍历历史记录
        for message in reversed(self.conversation_histories[user_id].messages):
            if isinstance(message, AIMessage):
                try:
                    # 尝试解析JSON内容
                    import json
                    content_data = json.loads(message.content)
                    if isinstance(content_data, dict) and content_data.get("type") == "summary":
                        return content_data.get("data", "")
                except (json.JSONDecodeError, TypeError):
                    # 如果不是JSON，检查字符串内容
                    if "summary" in message.content.lower():
                        return message.content

        return ""

    def _add_to_history(self, user_id: str, role: str, content: Any) -> None:
        """
        使用LangChain的方法添加对话历史
        """
        if not user_id:
            user_id = "anonymous"

        # 获取聊天历史
        chat_history = self._get_chat_history(user_id)

        # 序列化内容为字符串
        if isinstance(content, dict):
            import json
            content_str = json.dumps(content, ensure_ascii=False)
        else:
            content_str = str(content)

        # 根据角色添加消息
        if role == "user":
            chat_history.add_user_message(content_str)
        elif role == "assistant":
            chat_history.add_ai_message(content_str)
        elif role == "system":
            chat_history.add_message(SystemMessage(content=content_str))

        # 限制历史记录长度
        self._trim_history(user_id)

    def _trim_history(self, user_id: str, max_messages: int = 50) -> None:
        """修剪历史记录，保留最近的消息"""
        if not user_id:
            user_id = "anonymous"

        if user_id in self.conversation_histories:
            chat_history = self.conversation_histories[user_id]
            messages = chat_history.messages

            if len(messages) > max_messages:
                # 保留最近的消息
                recent_messages = messages[-max_messages:]
                chat_history.clear()
                for message in recent_messages:
                    chat_history.add_message(message)

    def clear_history(self, user_id: str) -> bool:
        """清空用户对话历史"""
        if not user_id:
            user_id = "anonymous"

        if user_id in self.conversation_histories:
            self.conversation_histories[user_id].clear()
            return True
        return False

    def export_history(self, user_id: str, filepath: str = None) -> str:
        """导出对话历史"""
        history = self.get_history(user_id)
        import json
        json_str = json.dumps(history, ensure_ascii=False, indent=2)

        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)

        return json_str


# 创建旅行顾问实例
new_travel_advisor = TravelAdvisor()