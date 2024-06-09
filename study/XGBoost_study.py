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
print(data1.head())

# NaN 값 제거
data1 = data1.dropna(axis=0)
# 필요한 컬럼 선택
dataset = data1[['y', '기온', '습도']]

# 데이터 정규화
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
def create_dataset(data, look_back=240):
    X, Y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), :-1].flatten())
        Y.append(data[i + look_back, -1])
    return np.array(X), np.array(Y)

look_back = 240
X, y = create_dataset(scaled_data, look_back)

# 데이터셋을 학습셋과 테스트셋으로 분리 (80% 학습, 20% 테스트)
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# XGBoost 모델 구축
'''model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

with open('xgboost_saved_model', 'wb') as f:
    pickle.dump(model, f)'''

with open('xgboost_saved_model', 'rb') as f:
    model = pickle.load(f)

# 예측 수행
predictions = model.predict(X_test)


# 데이터 반정규화
predictions = scaler.inverse_transform(np.concatenate((np.zeros((predictions.shape[0], 2)), predictions.reshape(-1, 1)), axis=1))[:, 2]
y_test = scaler.inverse_transform(np.concatenate((np.zeros((y_test.shape[0], 2)), y_test.reshape(-1, 1)), axis=1))[:, 2]


test_dates = data1['ds'][-len(y_test):]
test_Actual = data1['y'][-len(y_test):]


# 일부 예측값과 실제값을 비교하기 위해 데이터프레임 생성
comparison = pd.DataFrame({'Date': test_dates, 'test_Actual': test_Actual,'Actual': y_test, 'Predicted': predictions})

# 날짜를 인덱스로 설정
comparison.set_index('Date', inplace=True)

# 일부 샘플 출력 (예: 상위 10개)
print(comparison.tail(24))

# 결과 시각화
plt.figure(figsize=(14,5))
plt.plot(data.index[-len(y_test):], y_test, label='Actual Power Demand')
plt.plot(data.index[-len(y_test):], predictions, label='Predicted Power Demand')

#plt.plot(data.index[-240:], y_test, label='Actual Power Demand')
#plt.plot(data.index[-240:], predictions, label='Predicted Power Demand')

plt.xlabel('Date')
plt.ylabel('Power Demand')
plt.legend()
plt.show()

# 성능 평가
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
mape = mean_absolute_percentage_error(y_test, predictions)

print(f'RMSE: {rmse}')
print(f'MAPE: {mape}')
print(f'mse: {mse}')


test_dates = data1['ds'][-len(y_test):]
test_Actual = data1['y'][-len(y_test):]

