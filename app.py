from flask import Flask, g, request,make_response, jsonify
import os
import time
from flask_cors import CORS
from pyinstrument import Profiler

app = Flask(__name__)
cors = CORS(app)

@app.before_request
def before_request():
    if "profile" in request.args:
        g.profiler = Profiler()
        g.profiler.start()


@app.after_request
def after_request(response):
    if not hasattr(g, "profiler"):
        return response
    g.profiler.stop()
    output_html = g.profiler.output_html()
    return make_response(output_html)

def dbCall():
    time.sleep(3)
    productsdb = [
        { 'id': 0, 'title': 'Apples', 'price': 1.20 },
        { 'id': 1, 'title': 'Bananas', 'price': 1.45 },
        { 'id': 2, 'title': 'Grapes', 'price': 5.12 },
        { 'id': 3, 'title': 'Blackberries', 'price': 2.52 }
    ]
    return productsdb

@app.route('/', methods=['GET'])
def home():
    products = dbCall()
    return jsonify(products)


if __name__ == '__main__':
    port= os.environ.get('PORT')
    app.run(host='0.0.0.0', debug=True, port=port)
