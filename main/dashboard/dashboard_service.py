import requests
import xmltodict
import pandas as pd
import config


class dashboard_service:
    def supply_date(self):
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

        return data_r

    def get_smpPrice(self):
        url = f'https://openapi.kpx.or.kr/openapi/smp1hToday/getSmp1hToday?areaCd=1&serviceKey={config.serviceKey}'
        response = requests.get(url, verify=False)
        res = xmltodict.parse(response.text)

        smp_df = pd.DataFrame(res['response']['body']['items']['item'])
        smp_df = smp_df.drop(columns=['areaCd'])

        smp_df['smp'] = smp_df['smp'].astype(float)

        smp_df['timetable'] = pd.to_datetime(
            smp_df['tradeDay'].astype(str) + smp_df['tradeHour'].astype(str).str.zfill(2),
            format='%Y%m%d%H')#.dt.strftime('%Y-%m-%d %H')

        print('get_smpPrice')

        return smp_df
