import requests
import xmltodict
import pandas as pd
from api import config
from datetime import datetime


class dashboard_service:
    def supply_date(self):
        url = f'https://openapi.kpx.or.kr/openapi/sukub5mToday/getSukub5mToday?ServiceKey={config.serviceKey}'

        response = requests.get(url, verify=False)

        res = xmltodict.parse(response.text)

        supply_df = pd.DataFrame(res['response']['body']['items']['item'])

        print(supply_df.head())
        data = []
        b_hour = 0
        for row in supply_df.itertuples():
            baseDate = pd.to_datetime(getattr(row, 'baseDatetime')[:12])
            currPwrTot = float(getattr(row, 'currPwrTot'))
            hour = int(pd.to_datetime(getattr(row, 'baseDatetime')[:12]).hour)
            b_hour = hour
            data.append({
                '기준일시': baseDate,
                '현재수요': currPwrTot,
                '시간': hour
            })

        if b_hour < 23:
            base_date = datetime.today().strftime('%Y%m%d')  # 발표 일자

            base_time = 24 - b_hour

            for i in range(b_hour):

                if (i + base_time) > 9:
                    dt = str(base_date) + str(i + base_time) + "00"

                else:
                    dt = str(base_date) + "0" + str(i + base_time) + "00"

                data.append({
                    '기준일시': pd.to_datetime(dt)
                })

        df = pd.DataFrame(data)

        df['기준일시'] = pd.to_datetime(df['기준일시'])
        df.set_index('기준일시', inplace=True)
        data_r = df.resample('H').mean().reset_index()

        return data_r

    def get_smpPrice(self):
        url = f'https://openapi.kpx.or.kr/openapi/smp1hToday/getSmp1hToday?areaCd=1&serviceKey={config.serviceKey}'
        response = requests.get(url, verify=False)
        res = xmltodict.parse(response.text)

        smp_df = pd.DataFrame(res['response']['body']['items']['item'])
        print(smp_df.head())

        smp_df = smp_df.drop(columns=['areaCd'])

        smp_df['smp'] = smp_df['smp'].astype(float)


        smp_df['timetable'] = pd.to_datetime(
            smp_df['tradeDay'].astype(str) + smp_df['tradeHour'].astype(str).str.zfill(2),
            format='%Y%m%d%H')  # .dt.strftime('%Y-%m-%d %H')

        print('get_smpPrice')

        return smp_df
