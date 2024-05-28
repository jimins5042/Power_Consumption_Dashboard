import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import performance_metrics


class Predict_By_Prophet:


    def predict(self):
        df = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')
        df['기준일시'] = pd.to_datetime(df['기준일시'])
        df.set_index('기준일시', inplace=True)
        data_r = df.resample('D').mean()

        print(data_r.head())

        data_r = data_r.reset_index()
        data_r['ds'] = data_r['기준일시']
        data_r['y'] = data_r['현재수요(MW)']

        data1 = data_r[['ds', 'y']]
        data1 = data1[-2000:]

        print(data1.head())

        prophet_m = Prophet().fit(data1)

        future = prophet_m.make_future_dataframe(periods=30)
        future.tail()
        # 미래 가격 예측하기
        forecast = prophet_m.predict(future)

        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

        return forecast

