# -*- coding=utf-8 -*-
"""
    @project: Langchain_agent
    @Author：piyj
    @file： summary_templates.py
    @time：2025/8/26 10:22
"""


def get_summary_prompt(user_input: str, answers: dict) -> str:
    """
    获取生成旅行总结的提示词
    Args:
        user_input: 用户初始需求
        answers: 用户的问题答案

    Returns:
        提示词字符串
    """
    # 格式化答案信息
    answers_text = "\n".join([f"- {q}: {a}" for q, a in answers.items()])

    return f"""
你是一个专业的旅行规划师，请根据用户的初步需求和详细回答，生成一份完整的旅行需求总结。

# 用户初步需求
{user_input}

# 用户详细回答
{answers_text}

# 总结要求
1. 生成800字以内的纯文本内容
2. 内容结构清晰，包含以下部分：
   - 需求概述
   - 预算分析
   - 主题偏好
   - 时间安排建议
   - 目的地推荐思路
   - 旅行风格描述
   - 个性化建议

3. 语言风格：专业且友好，具有建设性
4. 避免使用markdown格式，使用纯文本
5. 基于用户的回答提供具体的建议

请生成旅行需求总结：
"""