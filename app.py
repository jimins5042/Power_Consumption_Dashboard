import pandas as pd
from flask import Flask, render_template, request, jsonify,Response
from tabulate import tabulate
from urllib import parse

import Chat_Bot
import Predict_By_Prophet

import json

from functools import wraps

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

p = Predict_By_Prophet.Predict_By_Prophet()
chat_res = Chat_Bot.Chat_bot()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict')
def predict_cal():
    data = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')

    data['기준일시'] = pd.to_datetime(data['기준일시'])

    data = data.dropna(axis=0)  # 0제거

    data = data[['기준일시', '현재수요(MW)']]
    data.set_index('기준일시', inplace=True)
    df1 = data.resample('D').mean().reset_index()

    df = p.predict()

    resampled_data = {
        'Month': df['ds'],
        'Dataset1': df['yhat'],
        'Dataset2': df['yhat_upper'],
        'Dataset3': df1['현재수요(MW)'],
        'Dataset4': df['yhat_lower'],
    }

    resampled_df = pd.DataFrame(resampled_data)

    param = request.args.get('param')
    param = int(param) * -1

    resampled_df = resampled_df[param:]
    print(resampled_df.head())
    return resampled_df.to_json(orient='split')


@app.route('/chat', methods=["GET"])
def chat():
    return render_template('chat.html')


@app.route('/chat', methods=["POST"])
def chat_rag():
    user_message = request.json
    response_message = generate_bot_response(user_message)

    #한국어 인코딩
    res = json.dumps(response_message, ensure_ascii=False).encode('utf8')
    return Response(res, content_type='application/json; charset=utf-8')

def generate_bot_response(user_message):
    # 간단한 봇 응답 로직 (필요에 따라 수정 가능)
    if user_message == "안녕":

        return "안녕하세요! 무엇을 도와드릴까요?"
    elif user_message == "도움말":
        return "명령어 목록: !구매, !다시, !공유"
    else:
        return "죄송해요, 이해하지 못했어요."



if __name__ == '__main__':
    app.run()
