import json
import time

from flask import render_template, request, Response, Blueprint
from api.main.chatbot.chatbot_service import chatbot_service

cb = Blueprint("chatbot_controller", __name__)
chat_res = chatbot_service()


class chatbot_controller:

    @cb.route('/chat', methods=["GET"])
    def chat():
        # return render_template('chat.html')
        return render_template('common_frame.html', filename='chatbot.html')

    @cb.route('/chat', methods=["POST"])
    def chat_rag():
        user_message = request.json
        start = time.time()
        response_message = chatbot_controller.generate_bot_response(user_message, 'chat')

        print(f"답변시간 : {time.time() - start:.5f} sec")

        # 한국어 인코딩
        res = json.dumps(response_message, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')

    @cb.route('/search', methods=["POST"])
    def similarity_search():

        user_message = request.json

        # 사용자 질문과 유사도가 높은 검색된 상위 3개의 문장, 유사도 받아오기
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
            if type == "chat":
                answer = chat_res.caching_embeds(user_message)

                '''
                time.sleep(5)
                answer = """RPS 제도란 공급의무자로 하여금 총 발전량의 일정 비율 이상을 신재생에너지로 공급할 의무를 부화하는 제도입니다.
                            RPS제도에 따라 공급의무자(대규모 발전사업자)는 총 발전량의 일정 비율을 신재생에너지로 공급해야합니다. 
                            RPS 공급의무자는 REC(인증서) 구매를 통해 신재생에너지 공급을 증명할 수 있습니다. 
                            SMP는 발전소(발전원 무관)가 전력을 판매할 때 적용되는 전력 자체의 가격입니다. 
                            신재생에너지 발전소 입장에서 생각하면, 주요 수익은 크게 REC 판매수익과 전력판매수익(SMP)으로 구분됩니다. 태양광 발전소 등 신재생에너지 발전소의 매출을 논할 때 'SMP+1REC 가격'이 소통의 기준이 되는 이유입니다. """
                            '''
            if type == "search":
                # string이 아닌 dataframe을 반환
                source = chat_res.caching_similar_search(user_message)
                return source

        return answer
