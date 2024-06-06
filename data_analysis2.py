import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate
from prophet import Prophet
from prophet.plot import add_changepoints_to_plot
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import performance_metrics

plt.rcParams['font.family'] = 'NanumGothic'  # 한글 폰트로 나눔고딕 설정

# CSV 파일 읽기
weather_df = pd.read_csv('C:/Users/김지민/Desktop/data/기상 데이터.csv')
supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')

# NaN 값을 확인하고 빈 문자열로 대체
weather_df = weather_df.fillna('')
supply_df = supply_df.fillna('')

# 필요한 데이터 추출 및 전처리
data = pd.concat([weather_df['일시'], weather_df['기온(°C)'], weather_df['습도(%)']], axis=1)
data_f = data[data['일시'] >= "2024-05-17 09:15:00"]
data = data[data['일시'] < "2024-05-17 09:15:00"]
print(data.tail())

# 기준일시를 datetime 형식으로 변환 및 인덱스로 설정
supply_df['기준일시'] = pd.to_datetime(supply_df['기준일시'])
supply_df.set_index('기준일시', inplace=True)
data_r = supply_df.resample('h').mean()

print(data_r.head())

# 데이터 병합 및 전처리
data_r = data_r.reset_index()
data_r['ds'] = data_r['기준일시']
data_r['y'] = data_r['현재수요(MW)']

# 데이터 길이 맞추기
min_length = min(len(data_r), len(data))
data_r = data_r.iloc[:min_length]
data = data.iloc[:min_length]

data_r['기온'] = data['기온(°C)'].values
data_r['습도'] = data['습도(%)'].values

data1 = data_r[['ds', 'y', '기온', '습도']]

# NaN 값 제거
data1 = data1.dropna(axis=0)

# 통계 정보 출력
statistics = {
    '표본 개수': data1.count(),
    '최소값': data1.min(),
    '최대값': data1.max(),
    '평균': data1.mean(),
    '표준편차': data1.std(),
    '결측치': data1.isnull().sum()
}
statistics_df = pd.DataFrame(statistics)
print(tabulate(statistics_df, headers='keys', tablefmt='psql', showindex=True))

# Prophet 모델 생성 및 학습
#prophet_m = Prophet()
prophet_m = (Prophet(changepoint_range=0.9,
                     changepoint_prior_scale=0.01,
                     interval_width=0.7
                     )
             .add_seasonality(name='weekly', period=7, fourier_order=10, prior_scale=0.1))
prophet_m.add_regressor('기온')
prophet_m.add_regressor('습도')
prophet_m.fit(data1)

# 미래 예측
future = prophet_m.make_future_dataframe(periods=240, freq='H')
future['기온'] = weather_df['기온(°C)'].values[:len(future)]
future['습도'] = weather_df['습도(%)'].values[:len(future)]

# 예측 수행
forecast = prophet_m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())


# 예측 결과 시각화
fig1 = prophet_m.plot(forecast)
a = add_changepoints_to_plot(fig1.gca(), prophet_m, forecast)
fig2 = prophet_m.plot_components(forecast)
fig1.show()
fig2.show()

# 교차 검증 및 성능 평가
df_n_cv = cross_validation(prophet_m, initial='365 days', period='90 days', horizon='240 hours')
df_n_p = performance_metrics(df_n_cv)
fig3 = plot_cross_validation_metric(df_n_cv, metric='mape')
print(df_n_p)

avg_rmse = df_n_p['rmse'].mean()
avg_mape = df_n_p['mape'].mean()
print("평균 RMSE: " + str(avg_rmse))
print("평균 MAPE: " + str(avg_mape))

# 예측 기간에 따른 MAPE(오차율) 표시
fig3.show()
