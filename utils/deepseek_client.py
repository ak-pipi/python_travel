from typing import Dict, Any, List
import json

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from conf.deepseek_conf_manager import config_manager

class DeepSeekClient:

    def __init__(self):
        config = config_manager.get_deepseek_config()

        # 使用LangChain的ChatOpenAI
        self.llm = ChatOpenAI(
            api_key=config['api_key'],
            base_url=config['api_base'],
            model=config['model_name'],
            temperature=config['temperature'],
            max_tokens=config['max_tokens']
        )

    def generate_questions(self, user_input: str) -> List[Dict]:
        """生成挖掘深层需求的问题"""
        from utils.prompt_templates import get_question_prompt
        prompt = get_question_prompt(user_input)
        try:
            response = self.llm.invoke(prompt)
            return self._parse_response(response.content)
        except Exception as e:
            print(f"生成问题时出错: {e}")
            return self._get_fallback_questions()
        # question_prompt = get_question_prompt()
        # prompt = PromptTemplate(
        #     input_variables=["user_input"],
        #     template=question_prompt
        # )
        # chain = prompt | self.llm
        # try:
        #     response = chain.invoke({"user_input": user_input})
        #     return self._parse_response(response.content)
        # except Exception as e:
        #     print(f"生成问题时出错: {e}")
        #     return self._get_fallback_questions()

    def _parse_response(self, response_text: str) -> List[Dict]:
        """使用JsonOutputParser解析模型响应"""
        try:
            # 创建JSON输出解析器
            parser = JsonOutputParser()

            # 清理响应文本
            cleaned_text = response_text.strip()
            if '```json' in cleaned_text:
                cleaned_text = cleaned_text.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned_text:
                cleaned_text = cleaned_text.split('```')[1].split('```')[0].strip()

            # 使用LangChain解析器
            parsed_data = parser.parse(cleaned_text)

            # 确保返回的是列表格式
            if isinstance(parsed_data, dict) and 'questions' in parsed_data:
                return parsed_data['questions']
            elif isinstance(parsed_data, list):
                return parsed_data
            else:
                raise OutputParserException("解析结果格式不正确")

        except OutputParserException as e:
            print(f"JSON解析错误: {e}")
            return self._get_fallback_questions()
        except Exception as e:
            print(f"解析响应时出错: {e}")
            return self._get_fallback_questions()

    # def _parse_response(self, response_text: str) -> List[Dict]:
    #     """解析模型响应"""
    #     try:
    #         # 尝试解析JSON
    #         if '```json' in response_text:
    #             json_str = response_text.split('```json')[1].split('```')[0].strip()
    #         else:
    #             json_str = response_text.strip()
    #
    #         questions = json.loads(json_str)
    #         return questions
    #     except json.JSONDecodeError:
    #         # 如果JSON解析失败，返回默认问题
    #         return self._get_fallback_questions()

    def _get_fallback_questions(self) -> List[Dict]:
        """获取备用问题列表"""
        return [
            {
                "question": "您的旅行预算是多少？",
                "dimension": "budget",
                "options": ["5000元以下", "5000-10000元", "10000-20000元", "20000元以上", "自定义"],
                "type": "single_choice"
            },
            {
                "question": "您偏好什么类型的旅行主题？",
                "dimension": "theme",
                "options": ["自然风光", "历史文化", "美食体验", "冒险运动", "休闲度假", "自定义"],
                "type": "multiple_choice"
            }
        ]


# 单例实例
deepseek_client = DeepSeekClient()


# if __name__ == '__main__':
#     deepseek_client = DeepSeekClient()
#     que = deepseek_client.generate_questions("我想去日本旅游")
#     print(que)