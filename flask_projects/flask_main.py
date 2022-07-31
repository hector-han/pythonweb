from flask import Flask
from flask import render_template, request
from utils import get_geo_result

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/geocoding", methods=['POST'])
def geocoding():
    address = request.form.get("address")
    ret = get_geo_result(address, '<br>')
    return ret
