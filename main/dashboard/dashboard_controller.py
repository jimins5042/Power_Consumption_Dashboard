import pandas as pd
from flask import render_template, Blueprint


from main.dashboard import dashboard_service, Predict_Model

ds = Blueprint("dashboard_controller", __name__)
service = dashboard_service.dashboard_service()


class dashboard_controller:
    p = Predict_Model.Predict_Model()

    @ds.route('/show')
    def show_graph():
        #return render_template('Graph.html')
        return render_template('dashboard.html')

    @ds.route('/predict')
    def predict_cal():
        supply_df = pd.read_csv('C:/Users/김지민/Desktop/data/HOME_전력수급_실시간전력수급.csv')
        supply_df['일시'] = pd.to_datetime(supply_df['일시'])
        supply_df.set_index('일시', inplace=True)
        df = supply_df.resample('H').mean().reset_index()

        data_r = service.supply_date()

        df['1일전'] = data_r['현재수요']

        #data_r['1일전'] = df['현재부하(MW)']
        print(data_r.head())

        # df = p.predict_XGBoost(data_r)
        resampled_data = {
            'Month': df['일시'].astype(str),
            'Dataset1': df['1일전'],
            'Dataset2': df['현재부하(MW)']
        }

        '''resampled_data = {
            'Month': data_r['기준일시'].astype(str),
            'Dataset1': data_r['1일전'],
            'Dataset2': data_r['현재수요']
        }'''

        resampled_df = pd.DataFrame(resampled_data)

        print(resampled_df.head())
        return resampled_df.to_json(orient='split')
