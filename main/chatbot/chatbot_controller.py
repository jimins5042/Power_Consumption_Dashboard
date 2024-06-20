import json

from flask import render_template, request, Response, Blueprint, jsonify
import pandas as pd
from main.chatbot.chatbot_service import chatbot_service

cb = Blueprint("chatbot_controller", __name__)
chat_res = chatbot_service()


class chatbot_controller:

    @cb.route('/chat', methods=["GET"])
    def chat():
        # return render_template('chat.html')
        return render_template('chatbot.html')

    @cb.route('/chat', methods=["POST"])
    def chat_rag():
        user_message = request.json

        response_message = chatbot_controller.generate_bot_response(user_message, 'chat')

        # 한국어 인코딩
        res = json.dumps(response_message, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')

    @cb.route('/search', methods=["POST"])
    def similarity_search():
        user_message = request.json

        source = chatbot_controller.generate_bot_response(user_message, 'search')
        print(source)

        return source.to_json(orient='split')


    def generate_bot_response(user_message, type):
        # 간단한 봇 응답 로직 (필요에 따라 수정 가능)

        answer = ''
        if user_message == "안녕":
            answer = "안녕하세요! 무엇을 도와드릴까요?"

        elif user_message == "!도움말":
            answer = "명령어 목록: !구매, !다시, !공유"

        elif user_message == "!임베딩":
            chat_res.caching_flies()
            answer = "자료 학습 완료!"

        else:
            if (type == "chat"):
                #answer = chat_res.caching_embeds(user_message)
                answer = "성공"
            if (type == "search"):
                source = chat_res.caching_similar_search(user_message)
                return source

        return answer
