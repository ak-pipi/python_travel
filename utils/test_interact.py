# -*- encoding:utf-8 -*-
"""
    @project: Langchain_agent
    @Author：piyj
    @file： test_interact.py
    @time：2025/8/26 14:23
"""
import requests

from utils.summary_generator import summary_generator


def test_summary_generation():
    """测试总结生成"""

    base_url = "http://127.0.0.1:8000"

    # 测试数据
    test_cases = [
        {
            "user_input": "我想去长沙旅游",
            "answers": {
                "预算": "5000-10000元",
                "时间": "5-7天",
                "主题": "休闲度假，美食体验",
                "目的地": "长沙",
                "同行人员": "情侣两人",
                "旅行风格": "舒适型，不喜欢太累"
            }
        }
        # {
        #     "user_input": "历史文化之旅",
        #     "answers": {
        #         "预算": "10000-15000元",
        #         "时间": "10天左右",
        #         "主题": "历史文化，古迹参观",
        #         "目的地": "西安、北京",
        #         "同行人员": "独自旅行",
        #         "旅行风格": "深度游，喜欢学习历史"
        #     }
        # }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 50}")
        print(f"测试用例 {i}")
        print(f"{'=' * 50}")

        # result = summary_generator.generate_travel_summary(
        #     test_case["user_input"],
        #     test_case["answers"]
        # )

        result = requests.post(f"{base_url}/api/travel/test_interact", json={
            "user_input": test_case["user_input"],
            "answers": test_case["answers"],
            "user_id": f"test_user_{i}"
        })
        result = result.json()

        if result["status"] == "success":
            print("✅ 生成成功!")
            print(f"📊 字数: {result['word_count']}")
            print(f"📝 总结内容:")
            print(result["summary"])
            print("\n🔑 关键点:")
            for key, value in result["key_points"].items():
                print(f"  {key}: {value}")
        else:
            print("❌ 生成失败:")
            print(result["message"])


if __name__ == "__main__":
    test_summary_generation()