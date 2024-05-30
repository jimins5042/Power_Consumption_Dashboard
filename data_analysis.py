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

df = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')

data = pd.concat(
    [df['공급능력(MW)'], df['현재수요(MW)'], df['최대예측수요(MW)'], df['공급예비력(MW)'], df['공급예비율(퍼센트)'], df['운영예비력(MW)'],
     df['운영예비율(퍼센트)']], axis=1)

list = ['공급능력(MW)', '현재수요(MW)', '최대예측수요(MW)', '공급예비력(MW)', '공급예비율(퍼센트)', '운영예비력(MW)', '운영예비율(퍼센트)']

for column in list:
    mean = data[column].mean()
    std = data[column].std()
    data = data[(data[column] >= mean - 4 * std) & (data[column] <= mean + 4 * std)]

statistics = {
    '표본 개수': data.count(),
    '최소값': data.min(),
    '최대값': data.max(),
    '평균': data.mean(),
    '표준편차': data.std(),
    '결측치': data.isnull().sum()
}

# 결과 출력
statistics_df = pd.DataFrame(statistics)

print(tabulate(statistics_df, headers='keys', tablefmt='psql', showindex=True))


def emwa(column, df):
    X = df[column]
    s = [X.iat[0]]
    c = [X.iat[0]]

    alpha = 0.3
    coefficient = 3

    for i in range(1, len(X)):
        c.append(X.iat[i])
        temp = alpha * X.iat[i] + (1 - alpha) * s[-1]
        s.append(temp)

    s_avg = np.mean(s)
    sigma = np.sqrt(np.var(X))
    ucl = s_avg + coefficient * sigma * np.sqrt(alpha / (2 - alpha))
    lcl = s_avg - coefficient * sigma * np.sqrt(alpha / (2 - alpha))

    print("평균 : " + str(s_avg) + ", 상한 : " + str(ucl) + ", 하한 : " + str(lcl))


'''for i in list:
    print("칼럼" + i)
    emwa(i)'''

df['기준일시'] = pd.to_datetime(df['기준일시'])
df.set_index('기준일시', inplace=True)
data_r = df.resample('D').mean()

print(data_r.head())

data_r = data_r.reset_index()
data_r['ds'] = data_r['기준일시']
data_r['y'] = data_r['현재수요(MW)']

data1 = data_r[['ds', 'y']]
data1 = data1[-1000:]

print(data1.head())

# prophet_m = Prophet().fit(data1)
#prophet_m = Prophet().add_seasonality(name='weekly', period=7, fourier_order=10, prior_scale=1).fit(data1)
# prophet_m = Prophet().add_seasonality(name='yearly', period= 365, fourier_order=10, prior_scale=0.1).fit(data1)
'''prophet_m = Prophet(seasonality_mode='additive',
                    seasonality_prior_scale=0.1,
                    changepoint_prior_scale=0.5).fit(data1)'''
'''
prophet_m = Prophet(seasonality_mode='additive',
                    seasonality_prior_scale=0.1,
                    changepoint_prior_scale=0.5).fit(data1)'''

prophet_m = (Prophet(changepoint_range=0.9,
                     changepoint_prior_scale=0.01,
                     interval_width=0.7
                     )
             .add_seasonality(name='weekly', period=7, fourier_order=10, prior_scale=0.1)
             .fit(data1))


future = prophet_m.make_future_dataframe(periods=30)
future.tail()
# 미래 가격 예측하기
forecast = prophet_m.predict(future)

print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

fig1 = prophet_m.plot(forecast)
a = add_changepoints_to_plot(fig1.gca(), prophet_m, forecast)

fig2 = prophet_m.plot_components(forecast)
'''start_date = '2024-01-01'
end_date = '2024-06-07'

ax = fig1.gca()
ax.set_xlim(pd.to_datetime([start_date, end_date]))'''

fig1.show()
fig2.show()
# df_n_cv = cross_validation(prophet_m, initial='300 days', period='60 days', horizon='30 days')
df_n_cv = cross_validation(prophet_m, initial='365 days', period='90 days', horizon='90 days')
df_n_p = performance_metrics(df_n_cv)
fig3 = plot_cross_validation_metric(df_n_cv, metric='mape')

print(df_n_p)
s = 0
for i in df_n_p['rmse']:
    s = s + i

print("평균 rmse : " + str(s / len(df_n_p['rmse'])))

s = 0
for i in df_n_p['mape']:
    s = s + i

print("평균 mape : " + str(s / len(df_n_p['rmse'])))

# 예측 기간에 따른 MAPE(오차율) 표시
fig3.show()
