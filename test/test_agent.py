# -*- encoding:utf-8 -*-
"""
    @project: Langchain_agent
    @Author：piyj
    @file： test_agent.py
    @time：2025/8/27 17:36
"""

# langchain 怎么创建agent智能体
from langchain.agents import create_openai_functions_agent, initialize_agent, AgentType
from langchain_core.runnables import Runnable
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents import Tool
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

from conf.deepseek_conf_manager import config_manager


@tool
def add(a: int, b: int) -> int:
    """两个数相加"""
    return a + b
@tool
def subtract(a: int, b: int) -> int:
    """两个数相减"""
    return a - b

tools = [
    Tool.from_function(
        func=add,
        name="add",
        description="两个数相加，返回结果"
    ),
    Tool.from_function(
        func=subtract,
        name="subtract",
        description="两个数相减，返回结果"
    )
]

def create_agent() -> Runnable:
    config = config_manager.get_deepseek_config()

    # 使用LangChain的ChatOpenAI
    llm = ChatOpenAI(
        api_key=config['api_key'],
        base_url=config['api_base'],
        model=config['model_name'],
        temperature=config['temperature'],
        max_tokens=config['max_tokens']
    )

    system_message = SystemMessage(content="你是一个数学助手，可以进行简单的加减运算。")
    human_message = HumanMessage(content="请使用提供的工具进行计算。")

    prompt = ChatPromptTemplate.from_messages([system_message, human_message])

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # 或者使用其他内置类型
        verbose=True,
        handle_parsing_errors=True
    )

    return agent
if __name__ == "__main__":
    agent = create_agent()
    user_input = "计算一下 5 + 3 - 2 的结果。"
    response = agent.invoke(user_input)
    print(f"Response: {response}")
#
