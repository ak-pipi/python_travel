# # -*- encoding:utf-8 -*-
# """
#     @project: Langchain_agent
#     @Author：piyj
#     @file： travel_plan_generator.py
#     @time：2025/8/26 14:49
# """
#
# from typing import Dict, Any
# from utils.travel_agent import get_travel_agent
# from utils.deepseek_client import deepseek_client
# import time
#
#
# class TravelPlanGenerator:
#     def __init__(self):
#         self.llm = deepseek_client.llm
#         self.agent = get_travel_agent()
#
#     def generate_detailed_plan(self, summary: str) -> Dict[str, Any]:
#         """
#         生成详细旅行攻略
#         Args:
#             summary: 用户需求总结
#         Returns:
#             旅行攻略结果
#         """
#         try:
#             start_time = time.time()
#
#             # 生成攻略
#             result = self.agent.generate_travel_plan(summary)
#
#             # 计算耗时
#             elapsed_time = time.time() - start_time
#
#             if result["status"] == "success":
#                 result["generation_time"] = round(elapsed_time, 2)
#                 result["message"] = "旅行攻略生成成功"
#
#                 # 添加质量评估
#                 quality_score = self._evaluate_plan_quality(result["plan_text"])
#                 result["quality_score"] = quality_score
#
#             return result
#
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"生成攻略时出错: {str(e)}",
#                 "plan_text": "",
#                 "structured_plan": {}
#             }
#
#     def _evaluate_plan_quality(self, plan_text: str) -> float:
#         """评估攻略质量"""
#         quality_score = 0.0
#
#         # 检查是否包含关键信息
#         key_elements = [
#             "交通", "住宿", "景点", "预算", "早餐", "午餐", "晚餐",
#             "第1天", "第2天", "第3天", "时间安排", "推荐"
#         ]
#
#         for element in key_elements:
#             if element in plan_text:
#                 quality_score += 0.5
#
#         # 限制最高分
#         return min(quality_score, 10.0)
#
#
# # 创建单例实例
# plan_generator = TravelPlanGenerator()