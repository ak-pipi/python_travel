
from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.travel_advisor import TravelAdvisor

app = Flask(__name__)
CORS(app)  # 允许跨域请求
# 创建旅行顾问实例
travel_advisor = TravelAdvisor()


@app.route('/api/travel/init', methods=['POST'])
def ask_questions():
    """接收用户输入并返回问题"""
    try:
        data = request.get_json()
        user_input = data.get('input', '').strip()
        user_id = data.get('user_id', 'anonymous')

        if not user_input:
            return jsonify({
                "status": "error",
                "message": "请输入旅行需求"
            }), 400

        result = travel_advisor.process_user_input(user_input, user_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"服务器错误: {str(e)}"
        }), 500


@app.route('/api/travel/answer', methods=['POST'])
def receive_answers():
    """接收用户答案"""
    try:
        data = request.get_json()
        answers = data.get('answers', {})
        user_id = data.get('user_id', 'anonymous')

        if not answers:
            return jsonify({
                "status": "error",
                "message": "请提供答案"
            }), 400

        result = travel_advisor.process_answers(answers, user_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"服务器错误: {str(e)}"
        }), 500


@app.route('/api/travel/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """获取对话历史"""
    try:
        history = travel_advisor.conversation_history.get(user_id, [])
        return jsonify({
            "status": "success",
            "history": history
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"获取历史时出错: {str(e)}"
        }), 500


@app.route('/api/travel/interact', methods=['POST'])
def generate_interact():
    """
    生成旅行需求总结接口
    """
    try:
        data = request.get_json()

        # 验证必要参数
        if not data or 'user_id' not in data or 'answers' not in data:
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: user_id 或 answers"
            }), 400

        user_id = data['user_id']
        answers = data['answers']

        # 验证答案格式
        if not isinstance(answers, dict):
            return jsonify({
                "status": "error",
                "message": "answers 参数必须是字典格式"
            }), 400

        # 生成总结
        result = travel_advisor.generate_travel_summary(user_id, answers)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"服务器错误: {str(e)}"
        }), 500


@app.route('/api/travel/test_interact', methods=['POST'])
def generate_test_interact():
    """
    测试生成旅行总结（不需要用户历史）
    """
    try:
        data = request.get_json()

        if not data or 'user_input' not in data or 'answers' not in data:
            return jsonify({
                "status": "error",
                "message": "缺少必要参数: user_input 或 answers"
            }), 400

        from utils.summary_generator import summary_generator

        result = summary_generator.generate_travel_summary(
            data['user_input'],
            data['answers']
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"服务器错误: {str(e)}"
        }), 500

#
# # @app.route('/api/travel/travel-research', mxethods=['POST'])
# # def generate_travel_plan():
# #     """
# #     生成旅行攻略接口
# #     """
# #     try:
# #         data = request.get_json()
# #
# #         if not data or 'user_id' not in data:
# #             return jsonify({
# #                 "status": "error",
# #                 "message": "缺少必要参数: user_id"
# #             }), 400
# #
# #         user_id = data['user_id']
# #
# #         # 生成攻略
# #         result = travel_advisor.generate_travel_plan(user_id)
# #
# #         return jsonify(result)
# #
# #     except Exception as e:
# #         return jsonify({
# #             "status": "error",
# #             "message": f"服务器错误: {str(e)}"
# #         }), 500
# #
# #
# # @app.route('/api/travel/travel-research-from-summary', methods=['POST'])
# # def generate_plan_from_summary():
# #     """
# #     直接从总结生成攻略（测试用）
# #     """
# #     try:
# #         data = request.get_json()
# #
# #         if not data or 'summary' not in data:
# #             return jsonify({
# #                 "status": "error",
# #                 "message": "缺少必要参数: summary"
# #             }), 400
# #
# #         from utils.travel_plan_generator import plan_generator
# #
# #         result = plan_generator.generate_detailed_plan(data['summary'])
# #
# #         return jsonify(result)
# #
# #     except Exception as e:
# #         return jsonify({
# #             "status": "error",
# #             "message": f"服务器错误: {str(e)}"
# #         }), 500
#
# @app.route('/health', methods=['GET'])
# def health_check():
#     """健康检查"""
#     return jsonify({"status": "healthy", "service": "travel_advisor"})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
    # lle = TravelAdvisor()
    # po = lle.process_user_input("我想去海边度假","test_user_1")
    # print(po)
    # # lle.process_answers({"您的旅行预算是多少？": "10000-20000元",
    # #     "您偏好什么类型的旅行主题？": ["自然风光", "美食体验"]})