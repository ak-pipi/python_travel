# -*- encoding:utf-8 -*-
"""
    @project: Langchain_agent
    @Author：piyj
    @file： summary_generator.py
    @time：2025/8/26 13:28
"""

from typing import Dict, Any, Optional
from utils.deepseek_client import deepseek_client
from utils.summary_templates import get_summary_prompt
import re


class SummaryGenerator:
    def __init__(self):
        self.min_length = 500  # 最小字数
        self.max_length = 800  # 最大字数

    def generate_travel_summary(self, user_input: str, answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成旅行需求总结

        Args:
            user_input: 用户初始需求
            answers: 用户的问题答案

        Returns:
            包含总结和元数据的字典
        """
        try:
            # 验证输入
            if not answers:
                return self._get_error_response("未提供答案数据")

            # 生成提示词
            prompt = get_summary_prompt(user_input, answers)

            # 调用AI生成总结
            print("🔄 正在生成旅行需求总结...")
            response = deepseek_client.llm.invoke(prompt)
            summary_text = response.content.strip()

            # 清理和验证总结内容
            cleaned_summary = self._clean_summary(summary_text)

            # 检查字数
            word_count = self._count_words(cleaned_summary)
            if word_count > self.max_length:
                cleaned_summary = self._truncate_summary(cleaned_summary)
                word_count = self._count_words(cleaned_summary)

            # 提取关键信息
            key_points = self._extract_key_points(cleaned_summary)

            return {
                "status": "success",
                "summary": cleaned_summary,
                "word_count": word_count,
                "key_points": key_points,
                "is_truncated": word_count >= self.max_length
            }

        except Exception as e:
            print(f"❌ 生成总结时出错: {e}")
            return self._get_error_response(f"生成总结时出错: {str(e)}")


    def _clean_summary(self, text: str) -> str:
        """清理总结文本"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text).strip()

        # 移除可能存在的markdown标记
        text = re.sub(r'[*#_\-]', '', text)

        # 确保以句号结束
        if not text.endswith(('.', '。', '!', '！', '?', '？')):
            text += '。'

        return text

    def _count_words(self, text: str) -> int:
        """计算中文字数"""
        # 中文单词计数（大致）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        # 非中文部分按空格分割
        other_parts = len(re.findall(r'\S+', re.sub(r'[\u4e00-\u9fff]', '', text)))
        return chinese_chars + other_parts

    def _truncate_summary(self, text: str) -> str:
        """截断超过字数限制的总结"""
        words = []
        current_count = 0

        # 简单的按句子截断
        sentences = re.split(r'[。！？.!?]', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            sentence_word_count = self._count_words(sentence)
            if current_count + sentence_word_count <= self.max_length:
                words.append(sentence)
                current_count += sentence_word_count
            else:
                break

        # 重新组合并确保完整性
        truncated_text = '。'.join(words) + '。'
        if self._count_words(truncated_text) < self.min_length:
            # 如果太短，返回原始文本的前800字
            truncated_text = text[:800] + '...'

        return truncated_text

    def _extract_key_points(self, summary: str) -> Dict[str, str]:
        """从总结中提取关键信息点"""
        key_points = {
            "budget": "未提及",
            "duration": "未提及",
            "theme": "未提及",
            "destination": "未提及"
        }

        # 简单的关键词提取
        budget_keywords = ['预算', '价格', '费用', '花费', '元', '钱']
        duration_keywords = ['天', '时间', '行程', '周期', '安排']
        theme_keywords = ['主题', '类型', '风格', '体验', '目的']
        destination_keywords = ['地方', '目的地', '城市', '国家', '地区', '景点']

        sentences = re.split(r'[。！？.!?]', summary)

        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence for keyword in budget_keywords):
                key_points["budget"] = sentence
            elif any(keyword in sentence for keyword in duration_keywords):
                key_points["duration"] = sentence
            elif any(keyword in sentence for keyword in theme_keywords):
                key_points["theme"] = sentence
            elif any(keyword in sentence for keyword in destination_keywords):
                key_points["destination"] = sentence

        return key_points

    def _get_error_response(self, message: str) -> Dict[str, Any]:
        """获取错误响应"""
        return {
            "status": "error",
            "summary": "",
            "message": message,
            "word_count": 0,
            "key_points": {},
            "is_truncated": False
        }


# 创建单例实例
summary_generator = SummaryGenerator()