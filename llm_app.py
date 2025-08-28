from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pkg.deepseek_conf import DeepSeekModel


def simpleDemo():
    llm_model = DeepSeekModel()
    # 1.定义模型
    # model = init_chat_model(
    #     model=llm_model.llm.model,
    #     api_key=llm_model.llm.api_key,
    #     api_base=llm_model.llm.api_base,
    #     temperature=llm_model.llm.temperature,
    #     max_tokens=llm_model.llm.max_tokens,
    #     # 模型提供商
    #     model_provider="deepseek",
    # )

    model = llm_model.llm

    # 2.定义提示词
    # prompt = [
    #     #  SystemMessage("Translate the following English text to Chinese"),
    #     SystemMessage("请将以下的内容翻译成汉语"),
    #     HumanMessage("Hello")
    # ]
    prompt = ChatPromptTemplate.from_messages([
        #  SystemMessage("Translate the following English text to Chinese"),
        ("请将以下的内容翻译成汉语"),
        # ("tesxt": "{input_data}")
        ("hello")
    ])
    # 3.定义输出字符串解析器(输出内容格式化，只需要结果部分)
    parser = StrOutputParser()
    # 4.创建链
    chain = prompt | model | parser
    input_data = {
        "text": "Hello, how are you?"
    }
    # 5.调用大模型
    response = chain.invoke(input_data)
    print(response)


if __name__ == "__main__":
    simpleDemo()