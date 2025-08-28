def get_question_prompt(user_input) -> str:
    """获取生成问题的提示词"""
    return f"""
你是一个专业的旅行顾问，需要根据用户的初步旅行需求，提出一些问题来挖掘深层需求。

用户初步需求: {user_input}

请生成3-5个问题，每个问题应该包含：
1. 问题文本
2. 所属维度（budget-预算, theme-主题偏好, duration-时间, route-路线, companion-旅伴, style-旅行风格）
3. 3-5个选项示例
4. 问题类型（single_choice-单选, multiple_choice-多选, text-文本）

请按照以下JSON格式返回：
[
  {{
    "question": "问题文本",
    "dimension": "维度",
    "options": ["选项1", "选项2", "选项3", "自定义"],
    "type": "问题类型"
  }}
]

请确保问题覆盖以下维度：
- 预算范围（budget）
- 旅行主题偏好（theme）
- 出行时间（duration）
- 路线偏好（route）
- 同行人员（companion）
- 旅行风格（style）

问题要具体、有针对性，选项要合理。
    """
