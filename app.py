from flask import Flask, render_template

from main.dashboard import dashboard_controller, Predict_Model
from main.chatbot import chatbot_controller

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
p = Predict_Model.Predict_Model()

# blueprint 설정
# 스프링은 이런거 안해도 알아서 잡아줬는데...
app.register_blueprint(dashboard_controller.ds)
app.register_blueprint(chatbot_controller.cb)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
