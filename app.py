from flask import Flask, render_template, request, Response, jsonify
import json
import pandas as pd
import Chat_Bot
import Predict_By_Prophet
import Predict_Model
import xmltodict
import requests
import config

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

p = Predict_Model.Predict_Model()
chat_res = Chat_Bot.Chat_bot()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show')
def show_graph():
    # return render_template('Graph.html')
    return render_template('dashboard.html')


@app.route('/predict')
def predict_cal():
    supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/HOME_전력수급_실시간전력수급.csv')
    supply_df['일시'] = pd.to_datetime(supply_df['일시'])
    supply_df.set_index('일시', inplace=True)
    data_r = supply_df.resample('H').mean().reset_index()

    # df = p.predict_XGBoost(data_r)

    resampled_data = {
        'Month': data_r['일시'].astype(str),
        'Dataset1': data_r['현재부하(MW)'],
        # 'Dataset2': df
        'Dataset2': data_r['현재부하(MW)']
    }

    resampled_df = pd.DataFrame(resampled_data)

    print(resampled_df.head())
    return resampled_df.to_json(orient='split')


def supply_date():
    url = f'https://openapi.kpx.or.kr/openapi/sukub5mToday/getSukub5mToday?ServiceKey={config.serviceKey}'

    response = requests.get(url, verify=False)

    res = xmltodict.parse(response.text)

    supply_df = pd.DataFrame(res['response']['body']['items']['item'])

    print(supply_df.head())
    data = []
    for row in supply_df.itertuples():
        baseDate = pd.to_datetime(getattr(row, 'baseDatetime')[:12])
        currPwrTot = float(getattr(row, 'currPwrTot'))
        hour = int(pd.to_datetime(getattr(row, 'baseDatetime')[:12]).hour)

        data.append({
            '기준일시': baseDate,
            '현재수요': currPwrTot,
            '시간': hour
        })
    df = pd.DataFrame(data)

    df['기준일시'] = pd.to_datetime(df['기준일시'])
    df.set_index('기준일시', inplace=True)
    data_r = df.resample('H').mean().reset_index()


@app.route('/chat', methods=["GET"])
def chat():
    return render_template('chat.html')


@app.route('/chat', methods=["POST"])
def chat_rag():
    user_message = request.json

    response_message = generate_bot_response(user_message)

    # 한국어 인코딩
    res = json.dumps(response_message, ensure_ascii=False).encode('utf8')
    return Response(res, content_type='application/json; charset=utf-8')


def generate_bot_response(user_message):
    # 간단한 봇 응답 로직 (필요에 따라 수정 가능)

    answer = ""
    if user_message == "안녕":
        answer = "안녕하세요! 무엇을 도와드릴까요?"

    elif user_message == "!도움말":
        answer = "명령어 목록: !구매, !다시, !공유"

    elif user_message == "!임베딩":
        chat_res.caching_flies()
        answer = "자료 학습 완료!"

    else:
        answer = chat_res.caching_embeds(user_message)

    return answer


if __name__ == '__main__':
    app.run()
