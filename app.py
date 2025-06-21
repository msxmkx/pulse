from flask import Flask, render_template_string, jsonify
import yfinance as yf
from datetime import datetime
import os

app = Flask(__name__)

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        previous_close = info.get('previousClose', current_price)
        change = current_price - previous_close
        change_percent = (change / previous_close * 100) if previous_close else 0
        return {
            'price': round(current_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'success': True
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return {
            'price': 0,
            'change': 0,
            'change_percent': 0,
            'success': False
        }

# HTML template for the main page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PULSE - Financial Intelligence Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #000;
            color: #fff;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid #333;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 3rem;
            font-weight: 300;
            letter-spacing: 8px;
            margin-bottom: 10px;
        }
        
        .tagline {
            font-size: 1.2rem;
            color: #888;
            font-weight: 300;
        }
        
        .market-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .market-card {
            background: #111;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #333;
            text-align: center;
        }
        
        .market-card h3 {
            color: #888;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .price {
            font-size: 2rem;
            font-weight: 300;
            margin-bottom: 5px;
        }
        
        .change {
            font-size: 1rem;
            font-weight: 500;
        }
        
        .positive { color: #00ff88; }
        .negative { color: #ff4444; }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        
        .feature-card {
            background: #111;
            padding: 30px;
            border-radius: 8px;
            border: 1px solid #333;
        }
        
        .feature-card h3 {
            color: #fff;
            font-size: 1.5rem;
            margin-bottom: 15px;
            font-weight: 400;
        }
        
        .feature-card p {
            color: #888;
            line-height: 1.6;
        }
        
        .status {
            text-align: center;
            padding: 20px;
            background: #111;
            border-radius: 8px;
            border: 1px solid #333;
            margin-top: 40px;
        }
        
        .status h3 {
            color: #00ff88;
            margin-bottom: 10px;
        }
        
        .status p {
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">PULSE</div>
            <div class="tagline">Professional Financial Intelligence Platform</div>
        </div>
        
        <div class="market-overview">
            <div class="market-card">
                <h3>S&P 500</h3>
                <div class="price" id="sp500-price">Loading...</div>
                <div class="change" id="sp500-change">--</div>
            </div>
            <div class="market-card">
                <h3>NASDAQ</h3>
                <div class="price" id="nasdaq-price">Loading...</div>
                <div class="change" id="nasdaq-change">--</div>
            </div>
            <div class="market-card">
                <h3>DOW JONES</h3>
                <div class="price" id="dow-price">Loading...</div>
                <div class="change" id="dow-change">--</div>
            </div>
            <div class="market-card">
                <h3>VIX</h3>
                <div class="price" id="vix-price">Loading...</div>
                <div class="change" id="vix-change">--</div>
            </div>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <h3>Real-Time Market Data</h3>
                <p>Access live stock prices, market indices, and real-time financial data with millisecond precision. Monitor market movements as they happen with our advanced data feeds.</p>
            </div>
            <div class="feature-card">
                <h3>Professional Analytics</h3>
                <p>Advanced technical analysis tools, portfolio performance tracking, and comprehensive market insights. Make informed investment decisions with institutional-grade analytics.</p>
            </div>
            <div class="feature-card">
                <h3>Market Intelligence</h3>
                <p>Stay ahead with curated financial news, market sentiment analysis, and emerging opportunity identification. Transform data into actionable investment intelligence.</p>
            </div>
        </div>
        
        <div class="status">
            <h3>✓ Platform Status: Operational</h3>
            <p>All systems functioning normally. Real-time data feeds active.</p>
        </div>
    </div>
    
    <script>
        function updateStockData(symbol, priceId, changeId) {
            fetch(`/stock/${symbol}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById(priceId).textContent = '$' + data.price.toLocaleString();
                        const changeElement = document.getElementById(changeId);
                        const changeText = (data.change >= 0 ? '+' : '') + data.change.toFixed(2) + 
                                         ' (' + (data.change_percent >= 0 ? '+' : '') + data.change_percent.toFixed(2) + '%)';
                        changeElement.textContent = changeText;
                        changeElement.className = 'change ' + (data.change >= 0 ? 'positive' : 'negative');
                    }
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }
        
        // Update market data every 30 seconds
        function updateAllData() {
            updateStockData('^GSPC', 'sp500-price', 'sp500-change');
            updateStockData('^IXIC', 'nasdaq-price', 'nasdaq-change');
            updateStockData('^DJI', 'dow-price', 'dow-change');
            updateStockData('^VIX', 'vix-price', 'vix-change');
        }
        
        // Initial load
        updateAllData();
        
        // Update every 30 seconds
        setInterval(updateAllData, 30000);
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/stock/<symbol>')
def stock_data(symbol):
    data = get_stock_price(symbol)
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 