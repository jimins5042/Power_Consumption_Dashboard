from datetime import datetime, timedelta
import json
import requests
import config
import pickle
import pandas as pd
import holidays
import xmltodict
import xml.etree.ElementTree as ET
import json

serviceKey = config.serviceKey
# --> 날씨를 알고 싶은 시간 입력
base_date = '20240616'  # 발표 일자
base_time = '2300'  # 발표 시간
nx = '62'  # 예보 지점 x좌표
ny = '123'  # 예보 지점 y좌표
# 알고 싶은 시간

# numOfRows 290일때 한페이지 당 24시간 데이터 조회 가능... 왜?

url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={serviceKey}&numOfRows=290&pageNo=1&dataType=json&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"

response = requests.get(url, verify=False)

res = response.json()
weather_df = pd.DataFrame(res['response']['body']['items']['item'])

weather_df['fcstValue'] = pd.to_numeric(weather_df['fcstValue'], errors='coerce')

pivot_df = weather_df.pivot_table(
    index=['baseDate', 'baseTime', 'fcstDate', 'fcstTime', 'nx', 'ny'],
    columns='category',
    values='fcstValue'
).reset_index()

# 결과 출력
print(pivot_df.head())


data = []
for row in pivot_df.itertuples():

    fcst_date = getattr(row, 'fcstDate')
    tmp_temp = float(getattr(row, 'TMP'))
    reh_temp = float(getattr(row, 'REH'))
    wsd_temp = float(getattr(row, 'WSD'))
    sky_temp = int(getattr(row, 'SKY'))

    if fcst_date in holidays.KR():
        holiday = 1
    else:
        holiday = 0

    hour = int(getattr(row, 'fcstTime')[:2])

    data.append({
        '날짜': fcst_date,
        '기온': tmp_temp,
        '습도': reh_temp,
        '풍속': wsd_temp,
        '전운량': sky_temp,
        '요일': datetime.strptime(fcst_date, '%Y%m%d').weekday() if fcst_date else None,
        '휴일': holiday,
        '시간': hour

    })

# Convert to DataFrame
df = pd.DataFrame(data)
print("?")
print(df.head())


# Convert to DataFrame
df = pd.DataFrame(data)
print(df.head())
# Load and process the supply data
supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/HOME_전력수급_실시간전력수급.csv')
supply_df['일시'] = pd.to_datetime(supply_df['일시'])
supply_df.set_index('일시', inplace=True)
data_r = supply_df.resample('H').mean().reset_index()

df['ds'] = data_r['일시']
df['1일전'] = data_r['현재부하(MW)']

data1 = df[['ds', '기온', '습도', '전운량', '풍속', '요일', '시간', '휴일', '1일전']]

# Display the result
print(data1.head())

with open('xgboost_saved_model_240516', 'rb') as f:
    model = pickle.load(f)
predictions = model.predict(data1.drop(columns=['ds']))

print(predictions)

