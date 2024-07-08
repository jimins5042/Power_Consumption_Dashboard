import pandas as pd
import holidays

kr_holidays = holidays.KR()
supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/통합 5분 단위 수급현황.csv')

supply_df['기준일시'] = pd.to_datetime(supply_df['기준일시'])
supply_df.set_index('기준일시', inplace=True)
date_data = supply_df.resample('h').mean()
date_data = date_data.reset_index()

print(date_data.head())

df = pd.DataFrame(columns=['날짜', '휴일여부'])
rows = []

for day in date_data['기준일시']:
    i = 0
    if day in kr_holidays:
        i = 1
        print(day, i)

    rows.append({'날짜': day, '휴일여부': i})

df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
df.to_csv('combined_data1.csv', index=False)


'''
# 빈 딕셔너리 생성
market_data = {}

# 각 파일을 불러와서 딕셔너리에 저장
for i in range(1, 8):

    market = 'file (' + str(i) + ")"

    market_data[market] = pd.read_csv(f'C:/Users/김지민/Desktop/새 폴더 (2)/{market}.csv',  encoding='cp949')

# 모든 데이터를 합치기
all_data = pd.concat(market_data.values(), ignore_index=True)

# csv 파일로 저장
all_data.to_csv('combined_data.csv', index=False)'''
