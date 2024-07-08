import pandas as pd
import requests
import xmltodict

from api import config

url = f'https://openapi.kpx.or.kr/openapi/smp1hToday/getSmp1hToday?areaCd=1&serviceKey={config.serviceKey}'
response = requests.get(url, verify=False)

res = xmltodict.parse(response.text)

supply_df = pd.DataFrame(res['response']['body']['items']['item'])
supply_df['timetable'] = pd.to_datetime(
    supply_df['tradeDay'].astype(str) + supply_df['tradeHour'].astype(str).str.zfill(2), format='%Y%m%d%H')
supply_df['timetable'] = supply_df['timetable'].dt.strftime('%Y-%m-%d %H')

print(supply_df.head())

'''
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

print(data_r.head())
'''
