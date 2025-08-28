# test_travel_advisor.py
import requests
import json


def test_travel_advisor():
    base_url = "http://127.0.0.1:8000"

    # 测试用例
    test_cases = [
        "我想去长沙旅游"
        # "计划一个历史文化之旅",
        # "和家人一起旅行，有小孩",
        # "预算有限的背包客旅行"
    ]

    for i, user_input in enumerate(test_cases):
        print(f"\n测试用例 {i + 1}: {user_input}")

        # 发送请求
        response = requests.post(f"{base_url}/api/travel/init", json={
            "input": user_input,
            "user_id": f"test_user_{i}"
        })

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                print("生成的问题:")
                for j, question in enumerate(data["questions"], 1):
                    print(f"  {j}. {question['question']}")
                    print(f"     选项: {', '.join(question['options'])}")
            else:
                print(f"错误: {data['message']}")
        else:
            print(f"请求失败: {response.status_code}")


if __name__ == "__main__":
    test_travel_advisor()