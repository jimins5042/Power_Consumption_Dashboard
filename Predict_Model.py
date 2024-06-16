import json
import pickle
from datetime import datetime

import holidays
import pandas as pd
import requests

import config


class Predict_Model:

    def predict_Prophet(self):
        with open('saved_model', 'rb') as f:
            prophet_m = pickle.load(f)

        future = prophet_m.make_future_dataframe(periods=30)
        future.tail()
        # 미래 가격 예측하기
        forecast = prophet_m.predict(future)

        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

        return forecast

    def predict_XGBoost(self, data_r):

        serviceKey = config.serviceKey

        base_date = '20240614'  # 발표 일자
        base_time = '2300'  # 발표 시간
        nx = '62'  # 예보 지점 x좌표
        ny = '123'  # 예보 지점 y좌표

        # numOfRows 290일때 한페이지 당 24시간 데이터 조회 가능... 왜?

        url = (f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={serviceKey}"
               f"&numOfRows=290&pageNo=1&dataType=json&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}")

        response = requests.get(url, verify=False)
        res = json.loads(response.text)

        informations = dict()
        for items in res['response']['body']['items']['item']:
            cate = items['category']
            fcstDate = items['fcstDate']
            fcstTime = items['fcstTime']
            fcstValue = items['fcstValue']
            temp = dict()
            temp[cate] = fcstValue

            if fcstTime not in informations:
                informations[fcstTime] = {'fcstDate': fcstDate}

            informations[fcstTime][cate] = fcstValue

        print(informations)

        isholiday = 0
        if fcstDate in holidays.KR():
            isholiday = 1

        data = []
        for key, val in informations.items():
            fcst_date = val.get('fcstDate', '')
            tmp_temp = float(val.get('TMP', 0))
            reh_temp = float(val.get('REH', 0))
            wsd_temp = float(val.get('WSD', 0))
            sky_temp = int(val.get('SKY', 0))
            hour = int(key[:2])
            minute = int(key[2:])

            data.append({
                '날짜': fcst_date,
                '기온': tmp_temp,
                '습도': reh_temp,
                '풍속': wsd_temp,
                '전운량': sky_temp,
                '요일': datetime.strptime(fcst_date, '%Y%m%d').weekday() if fcst_date else None,
                '휴일': isholiday,
                '시간': hour
            })

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Load and process the supply data
        '''supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/HOME_전력수급_실시간전력수급.csv')
        supply_df['일시'] = pd.to_datetime(supply_df['일시'])
        supply_df.set_index('일시', inplace=True)
        data_r = supply_df.resample('H').mean().reset_index()'''

        df['ds'] = data_r['일시']
        df['1일전'] = data_r['현재부하(MW)']

        data1 = df[['ds', '기온', '습도', '전운량', '풍속', '요일', '시간', '휴일', '1일전']]

        # Display the result
        print(data1.head())

        with open('xgboost_saved_model_240516', 'rb') as f:
            model = pickle.load(f)
        predictions = model.predict(data1.drop(columns=['ds']))

        print(predictions)
        return predictions
