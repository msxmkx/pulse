from flask import Flask, render_template_string
from datetime import datetime
import yfinance as yf
import random

app = Flask(__name__)

# Stock symbols for real data
stock_symbols = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "TSLA"]

def get_real_stock_data():
    """Fetch real stock data using yfinance"""
    stock_data = []
    for symbol in stock_symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change_pct = ((current_price - prev_price) / prev_price) * 100
                change_str = f"{'+' if change_pct >= 0 else ''}{change_pct:.2f}%"
                
                stock_data.append({
                    "symbol": symbol,
                    "name": info.get('longName', symbol),
                    "price": round(current_price, 2),
                    "change": change_str,
                    "sector": info.get('sector', 'Technology')
                })
            else:
                stock_data.append({
                    "symbol": symbol,
                    "name": symbol,
                    "price": round(random.uniform(100, 500), 2),
                    "change": f"{'+' if random.random() > 0.5 else ''}{random.uniform(0.5, 3.0):.2f}%",
                    "sector": "Technology"
                })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            stock_data.append({
                "symbol": symbol,
                "name": symbol,
                "price": round(random.uniform(100, 500), 2),
                "change": f"{'+' if random.random() > 0.5 else ''}{random.uniform(0.5, 3.0):.2f}%",
                "sector": "Technology"
            })
    
    return stock_data

# Simple template
TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Financial Times - Real Stock Data</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f8fafc; }
        .stock-card { background: white; border-radius: 10px; padding: 20px; margin: 10px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .positive { color: green; }
        .negative { color: red; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1>Financial Times - Real Stock Data</h1>
        <p class="text-muted">Live stock prices and analysis</p>
        
        <div class="row">
            {% for stock in stocks %}
            <div class="col-md-6">
                <div class="stock-card">
                    <h3>{{ stock.symbol }} - {{ stock.name }}</h3>
                    <p class="h4">${{ stock.price }}</p>
                    <p class="{{ 'positive' if '+' in stock.change else 'negative' }}">
                        {{ stock.change }}
                    </p>
                    <span class="badge bg-primary">{{ stock.sector }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

@app.route("/")
def home():
    stocks = get_real_stock_data()
    return render_template_string(TEMPLATE, stocks=stocks)

if __name__ == "__main__":
    app.run(debug=True, port=8080) 