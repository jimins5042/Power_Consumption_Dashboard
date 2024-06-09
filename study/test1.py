import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import pickle

# 데이터 로드 (예: CSV 파일)
plt.rcParams['font.family'] = 'NanumGothic'  # 한글 폰트로 나눔고딕 설정

# CSV 파일 읽기
weather_df = pd.read_csv('C:/Users/김지민/Desktop/data/기상 데이터 - 복사본.csv')
supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')

# NaN 값을 확인하고 빈 문자열로 대체
weather_df = weather_df.fillna('')
supply_df = supply_df.fillna('')

# 필요한 데이터 추출 및 전처리
data = pd.concat([weather_df['일시'], weather_df['기온(°C)'], weather_df['습도(%)'], weather_df['요일']], axis=1)
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

data_r['요일'] = data['요일'].values

data1 = data_r[['ds', 'y', '기온', '습도', '요일']]

# NaN 값 제거
data1 = data1.dropna(axis=0)
# 필요한 컬럼 선택
dataset = data1[['y', '기온', '습도', '요일']]

# 데이터셋을 학습셋과 테스트셋으로 분리 (80% 학습, 20% 테스트)
train_size = int(len(dataset) * 0.8)
train_set, test_set = dataset.iloc[:train_size], dataset.iloc[train_size:]

# XGBoost 모델 구축
model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
model.fit(train_set.drop(columns=['y']), train_set['y'])

with open('xgboost_saved_model2', 'wb') as f:
    pickle.dump(model, f)
# 예측 수행
predictions = model.predict(test_set.drop(columns=['y']))

# 결과 시각화
plt.figure(figsize=(14,5))
plt.plot(test_set.index, test_set['y'], label='Actual Power Demand')
plt.plot(test_set.index, predictions, label='Predicted Power Demand')
plt.xlabel('Date')
plt.ylabel('Power Demand')
plt.legend()
plt.show()

# 성능 평가
mse = mean_squared_error(test_set['y'], predictions)
rmse = np.sqrt(mse)
mape = mean_absolute_percentage_error(test_set['y'], predictions)

print(f'RMSE: {rmse}')
print(f'MAPE: {mape}')
print(f'MSE: {mse}')


comparison = pd.DataFrame({
    'Date': test_set.index,
    'Actual Power Demand': test_set['y'].values,
    'Predicted Power Demand': predictions
})

# 날짜를 인덱스로 설정
comparison.set_index('Date', inplace=True)

# 일부 샘플 출력 (예: 상위 10개)
print(comparison.head(10))