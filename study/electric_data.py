import pandas as pd
import requests
import xmltodict

import config

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
