# services/api_service.py
from itertools import chain
from threading import main_thread

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from conf.deepseek_conf_manager import config_manager



class DeepSeekModel:
    """
    DeepSeek配置管理模块，用于加载和管理DeepSeek相关配置
    """
    def __init__(self):
        config = config_manager.get_deepseek_config()

        # 使用LangChain的ChatOpenAI（如果DeepSeek兼容OpenAI API）
        self.llm = ChatOpenAI(
            api_key=config['api_key'],
            base_url=config['api_base'],
            model=config['model_name'],
            temperature=config['temperature'],
            max_tokens=config['max_tokens']
        )


    def test_api_key(self):
        """ 测试API Key是否有效"""
        try:
            # 定义解析器
            parser = StrOutputParser()
            # 定义提示词
            # 正确的提示词模板定义
            prompt = ChatPromptTemplate.from_messages([
                ("system", "你是一个专业的翻译官，擅长中英互译。"),
                ("human", "请将以下内容翻译成中文: {text}")
            ])
            # 创建链
            chain = prompt | self.llm | parser
            # 调用链以验证API Key
            # 尝试调用模型以验证API Key
            response = chain.invoke({"text": "Hello, world!"})
            # 如果调用成功，response应该是一个有效的响应对象
            if isinstance(response, str):
                print(f"✅ API Key 验证成功")
                print(f"📝 翻译结果: {response}")
            else:
                print("API Key验证失败，响应类型不正确")
            # 如果response不为None，则表示API Key有效
            return response is not None
        except Exception as e:
            print(f"❌ API Key 验证失败: {e}")
            return False


if __name__ == '__main__':

    ll = DeepSeekModel()
    ll.test_api_key()

    # 这里可以添加更多的逻辑来使用加载的配置
    # 例如，初始化模型等
    # model = init_chat_model(
    #     model=config.get("model", "deepseek-chat"),
    #     api_key=config.get("api_key", ""),
    #     api_base=config.get("api_base", "https://api.deepseek.com/"),
    #     temperature=float(config.get("temperature", 0.8)),
    #     max_tokens=int(config.get("max_tokens", 1024)),
    #     model_provider=config.get("model_provider", "deepseek"),
    # )
