import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Alpha Vantage API Key (replace with your own)
API_KEY = 'YOUR_ALPHAVANTAGE_API_KEY'

# In-memory portfolio
portfolio = {}

# Fetch stock data from Alpha Vantage API
def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if "Time Series (5min)" in data:
        latest_time = list(data["Time Series (5min)"].keys())[0]
        stock_info = data["Time Series (5min)"][latest_time]
        return {
            'symbol': symbol,
            'price': stock_info['1. open'],
            'time': latest_time
        }
    else:
        return None

# Homepage route
@app.route('/')
def index():
    return render_template('index.html', portfolio=portfolio)

# Add stock route
@app.route('/add', methods=['POST'])
def add_stock():
    symbol = request.form.get('symbol')
    if symbol and symbol not in portfolio:
        stock_data = fetch_stock_data(symbol.upper())
        if stock_data:
            portfolio[symbol.upper()] = stock_data
    return redirect(url_for('index'))

# Remove stock route
@app.route('/remove/<symbol>', methods=['GET'])
def remove_stock(symbol):
    if symbol in portfolio:
        del portfolio[symbol]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
