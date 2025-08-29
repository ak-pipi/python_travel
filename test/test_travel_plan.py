# -*- encoding:utf-8 -*-
"""
    @project: Langchain_agent
    @Author：piyj
    @file： test_travel_plan.py
    @time：2025/8/26 14:57
"""
import requests
from openai import base_url

from utils.travel_agent import tavily_searcher, tavily_agent


def test_travel_plan_generation():
    """测试旅行攻略生成"""

    base_url = "http://127.0.0.1:8000"

    test_summaries = [
        # """
        # 用户希望进行一个5天的海边度假旅行，预算8000元左右。
        # 偏好休闲度假和美食体验，希望去国内的海边城市。
        # 同行人员为情侣两人，喜欢舒适型的旅行风格，不喜欢太累的行程。
        # """,

        """
        用户计划一个7天的历史文化之旅，预算12000元。
        主要兴趣是参观历史古迹和学习文化，目的地偏好西安和北京。
        独自旅行，喜欢深度游，对历史有浓厚兴趣。
        """

        # """
        # 家庭旅行需求：4天3晚，带两个小孩（5岁和8岁）。
        # 预算6000元，希望有亲子活动和教育意义的地方。
        # 偏好自然风光和互动体验，交通要方便，住宿要家庭友好。
        # """
    ]

    for i, summary in enumerate(test_summaries, 1):
        print(f"\n{'=' * 60}")
        print(f"测试用例 {i}")
        print(f"{'=' * 60}")
        print(f"需求总结: {summary[:200]}...")
        result = requests.post(f"{base_url}/api/travel/travel-research-from-summary", json={
            "summary": summary,
            "user_id": f"test_user_{i}"
        })

        print(result.json())
        if result.status_code == 200:
            result_data = result.json()
            print("✅ 攻略生成成功!")
            print(f"⏱️  生成时间: {result_data.get('generation_time', 0)}秒")
            print(f"📊 字数: {result_data.get('word_count', 0)}")
            print(f"⭐ 质量评分: {result_data.get('quality_score', 0)}/10")
            print(f"🔍 使用搜索: {result_data.get('search_used', False)}")

            print("\n📝 攻略内容:")
            print(result_data.get("plan_text")[:500] + "..." if len(result_data.get("plan_text")) > 500 else result_data.get("plan_text"))

            # 显示结构化信息
            structured = result_data.get("structured_plan", {})
            if structured.get("days"):
                print(f"\n🗓️  行程天数: {len(structured['days'])}天")

        else:
            print("❌ 生成失败:")
            print(result.get("message", "未知错误"))


if __name__ == "__main__":
    test_travel_plan_generation()