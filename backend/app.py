
from flask import Flask, request, jsonify
import pandas as pd
from model import forecast_price 
import numpy as np

app = Flask(__name__)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

df = pd.read_csv('RS_Session_260_AU_1830_1.csv')
df.fillna(np.nan, inplace=True)
df = df.dropna()
@app.route('/test', methods=['GET'])
def test_route():
    return "Test route is working!",200
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    commodity = data['commodity']
    state_ut = data['state_ut']
    forecast_year = data['forecast_year']
    
    try:
        predicted_price = forecast_price(df, commodity, state_ut, forecast_year)
        return jsonify({'predicted_price': predicted_price})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
