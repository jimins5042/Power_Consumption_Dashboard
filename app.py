from flask import Flask, render_template, request, redirect, jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def cal():
    data = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')


    #data['기준일시'] = data['기준일시'].astype('int').astype('str')
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


if __name__ == '__main__':
    app.run()
