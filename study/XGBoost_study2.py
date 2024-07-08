import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import pickle


def cal(date):
    # 데이터 로드 (예: CSV 파일)
    plt.rcParams['font.family'] = 'NanumGothic'  # 한글 폰트로 나눔고딕 설정

    # CSV 파일 읽기
    weather_df = pd.read_csv('C:/Users/김지민/Desktop/data/기상 데이터 - 복사본.csv')
    supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')

    # NaN 값을 확인하고 빈 문자열로 대체
    # weather_df = weather_df.fillna('')
    supply_df = supply_df.fillna('')

    # 필요한 데이터 추출 및 전처리
    data = pd.concat([weather_df['일시'], weather_df['기온(°C)'], weather_df['습도(%)'], weather_df['요일'],
                      weather_df['시간'], weather_df['월'], weather_df['전운량(10분위)'], weather_df['풍속(m/s)'],
                      weather_df['휴일여부']],
                     axis=1)
    data = data.ffill()

    # 기준일시를 datetime 형식으로 변환 및 인덱스로 설정
    supply_df['기준일시'] = pd.to_datetime(supply_df['기준일시'])
    supply_df.set_index('기준일시', inplace=True)
    data_r = supply_df.resample('h').mean()

    # 데이터 병합 및 전처리
    data_r = data_r.reset_index()
    data_r['ds'] = data_r['기준일시']
    data_r['y'] = data_r['현재수요(MW)']

    data_r['7일전'] = data_r['7일전전력수요']
    data_r['1일전'] = data_r['1일전전력수요']

    # 데이터 길이 맞추기
    min_length = min(len(data_r), len(data))
    data_r = data_r.iloc[:min_length]
    data = data.iloc[:min_length]

    data_r['기온'] = data['기온(°C)'].values
    data_r['습도'] = data['습도(%)'].values

    data_r['요일'] = data['요일'].values
    data_r['시간'] = data['시간'].values
    data_r['월'] = data['월'].values
    data_r['전운량'] = data['전운량(10분위)'].astype(int).values
    data_r['풍속'] = data['풍속(m/s)'].astype(int).values
    data_r['휴일'] = data['휴일여부'].astype(int).values

    data1 = data_r[['ds', 'y', '기온', '습도', '풍속', '전운량','요일', '시간', '휴일', '1일전']]
    # data1 = data_r[['ds', 'y', '기온', '습도', '요일', '시간', '1일전']]
    # data1 = data1.dropna(axis=0)
    data1 = data1.ffill()

    test_set = data1[data1['ds'] >= date]
    train_set = data1[data1['ds'] < date]

    train_set = train_set.drop(columns=['ds'])
    test_set = test_set.drop(columns=['ds'])
    # print(test_set.head())

    # 필요한 컬럼 선택
    # dataset = data1[['y', '기온', '습도', '요일', '시간', '1일전']]

    # print(dataset.head())

    # 데이터셋을 학습셋과 테스트셋으로 분리
    '''
    train_size = int(len(dataset) * 0.8)
    train_set, test_set = dataset.iloc[:train_size], dataset.iloc[train_size:]'''

    # XGBoost 모델 구축
    model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1,
                         max_depth=8, subsample=0.8, min_child_weight=1, gamma=0.01)
    model.fit(train_set.drop(columns=['y']), train_set['y'])

    with open('xgboost_saved_model2', 'wb') as f:
        pickle.dump(model, f)
    # 예측 수행
    predictions = model.predict(test_set.drop(columns=['y']))

    # 결과 시각화
    '''plt.figure(figsize=(14, 5))
    plt.plot(test_set.index, test_set['y'], label='실제 전력 수요')
    plt.plot(test_set.index, predictions, label='예상 전력 수요')
    plt.xlabel('날짜')
    plt.ylabel('전력 수요')
    plt.legend()
    plt.show()'''

    # 성능 평가
    mse = mean_squared_error(test_set['y'][:240], predictions[:240])
    rmse = np.sqrt(mse)
    mape = mean_absolute_percentage_error(test_set['y'][:240], predictions[:240])
    # 정확도 계산 (허용 오차를 10%로 설정)
    tolerance = 0.10


    print(f'RMSE: {rmse}')
    print(f'MAPE: {mape}')
    print(f'MSE: {mse}')


    return rmse, mape

    '''comparison = pd.DataFrame({
        'Date': test_set.index,
        'Actual Power Demand': test_set['y'].values,
        'Predicted Power Demand': predictions
    })

    # 날짜를 인덱스로 설정
    comparison.set_index('Date', inplace=True)

    # 일부 샘플 출력 (예: 상위 10개)
    print(comparison.head(10))'''


list = {"2023-05-01",
        "2023-06-01",
        "2023-07-01",
        "2023-08-01",
        "2023-09-01",
        "2023-10-01",
        "2023-11-01",
        "2023-12-01",
        "2024-01-01",
        "2024-02-01",
        "2024-03-01",
        "2024-04-01",
        "2024-05-01"}

rmse = 0
mape = 0
for i in list:
    print(i)
    x, y, z = cal(i)
    rmse = rmse + x
    mape = mape + y

    time.sleep(1)
    
rmse = rmse/len(list)
mape = mape/len(list)

print("\n 전체 평균")
print(f'RMSE: {rmse}')
print(f'MAPE: {mape}')

