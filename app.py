import pandas as pd
from flask import Flask, render_template, request
from tabulate import tabulate
import Predict_By_Prophet

app = Flask(__name__)
p = Predict_By_Prophet.Predict_By_Prophet()


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


if __name__ == '__main__':
    app.run()
