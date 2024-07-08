import pandas as pd
from flask import render_template, Blueprint

from main.dashboard import Predict_Model, dashboard_service

ds = Blueprint("dashboard_controller", __name__)
service = dashboard_service.dashboard_service()
p = Predict_Model.Predict_Model()


class dashboard_controller:

    @ds.route('/show', methods=['GET'])
    def show_graph():
        # return render_template('Graph.html')

        return render_template('common_frame.html', filename='dashboard.html')

    @ds.route('/show', methods=['POST'])
    def predict_cal():
        supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/HOME_전력수급_실시간전력수급.csv')
        supply_df['일시'] = pd.to_datetime(supply_df['일시'])
        supply_df.set_index('일시', inplace=True)
        df = supply_df.resample('H').mean().reset_index()

        data_r = service.supply_date()

        # df['1일전'] = data_r['현재수요']

        # data_r['1일전'] = df['현재부하(MW)']
        print(data_r.tail())
        predictions = p.predict_XGBoost(df)  # 예상 값

        '''resampled_data = {
            'Month': df['일시'].astype(str),
            'Dataset1': df['현재부하(MW)'],
            'Dataset2': df['현재부하(MW)']
        }'''

        # 전력거래소 api 사용시 -> 하루 100회 제한
        resampled_data = {
            'Month': data_r['기준일시'].astype(str),
            'Dataset1': data_r['현재수요'],
            'Dataset2': predictions
        }

        resampled_df = pd.DataFrame(resampled_data)

        print(resampled_df.head())
        return resampled_df.to_json(orient='split')

    @ds.route('/power', methods=['GET'])
    def SMP():
        print('SMP')

        return render_template('common_frame.html', filename='power_transaction.html')

    @ds.route('/power', methods=['POST'])
    def show_SMP():
        print("show_SMP")
        smp_df = service.get_smpPrice()

        stock_data = {
            "Month": smp_df['timetable'].astype(str),
            # "Month": smp_df['tradeHour'].astype(str),
            "Dataset1": smp_df['smp']
        }

        stock_data = pd.DataFrame(stock_data)
        print(stock_data.tail())
        print("smp 데이터 전송 끝")
        return stock_data.to_json(orient='split')
