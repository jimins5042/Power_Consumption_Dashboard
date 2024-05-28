from flask import Flask, render_template, request, redirect, jsonify
import numpy as np
import pandas as pd

import Predict_By_Prophet

app = Flask(__name__)
p = Predict_By_Prophet.Predict_By_Prophet()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def cal():
    data = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')

    # data['기준일시'] = data['기준일시'].astype('int').astype('str')
    data['기준일시'] = pd.to_datetime(data['기준일시'])

    data = data.dropna(axis=0)  # 0제거

    data = data[['기준일시', '공급능력(MW)', '현재수요(MW)']]
    data.set_index('기준일시', inplace=True)
    df = data.resample('W').mean().reset_index()

    resampled_data = {
        'Month': df['기준일시'],
        'Dataset1': df['공급능력(MW)'],
        'Dataset2': df['현재수요(MW)']
    }
    resampled_df = pd.DataFrame(resampled_data)
    print(resampled_df.head())
    return resampled_df.to_json(orient='split')


@app.route('/data2')
def predict_cal():
    data = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')

    # data['기준일시'] = data['기준일시'].astype('int').astype('str')
    data['기준일시'] = pd.to_datetime(data['기준일시'])

    data = data.dropna(axis=0)  # 0제거

    data = data[['기준일시', '현재수요(MW)']]
    data.set_index('기준일시', inplace=True)
    df1 = data.resample('D').mean().reset_index()


    df = p.predict()

    resampled_data = {
        'Month': df['ds'],
        'Dataset1': df['yhat'],
        'Dataset2': df['yhat_lower'],
        'Dataset3': df['yhat_upper'],
        'Dataset4': df1['현재수요(MW)']
    }
    resampled_df = pd.DataFrame(resampled_data)
    resampled_df = resampled_df[-365:]
    print(resampled_df.head())
    return resampled_df.to_json(orient='split')


if __name__ == '__main__':
    app.run()
