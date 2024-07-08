from flask import Flask, render_template

from main.chatbot import chatbot_controller
from main.dashboard import dashboard_controller

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# blueprint 설정
app.register_blueprint(dashboard_controller.ds)
app.register_blueprint(chatbot_controller.cb)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shopping():
    products = [
        {
            "name": "Special Item",
            "image": "https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            "price": "$18.00",
            "old_price": "$20.00",
            "rating": 5,
            "on_sale": True
        },
        {
            "name": "Another Item",
            "image": "https://dummyimage.com/450x300/dee2e6/6c757d.jpg",
            "price": "$25.00",
            "old_price": "",
            "rating": 4,
            "on_sale": False
        }
        # Add more products as needed
    ]
    return render_template('shop.html', products=products)


'''
if __name__ == '__main__':
    app.run()
'''