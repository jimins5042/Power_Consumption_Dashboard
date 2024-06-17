import pickle
import pandas as pd
from prophet import Prophet


class Predict_By_Prophet:

    def save_predict_model(self):
        df = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')
        df['기준일시'] = pd.to_datetime(df['기준일시'])

        df.set_index('기준일시', inplace=True)

        data_r = df.resample('D').mean()

        print(data_r.tail())

        data_r = data_r.reset_index()
        data_r['ds'] = data_r['기준일시']
        data_r['y'] = data_r['현재수요(MW)']

        data1 = data_r[['ds', 'y']]
        data1 = data1[-2000:]

        print(data1.head())

        prophet_m = Prophet().add_seasonality(name='weekly', period=7, fourier_order=10, prior_scale=1).fit(data1)
        with open('main/dashboard/saved_model', 'wb') as f:
            pickle.dump(prophet_m, f)

    def predict(self):
        with open('main/dashboard/saved_model', 'rb') as f:
            prophet_m = pickle.load(f)

        future = prophet_m.make_future_dataframe(periods=30)
        future.tail()
        # 미래 가격 예측하기
        forecast = prophet_m.predict(future)

        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

        return forecast
