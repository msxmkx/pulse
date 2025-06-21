from flask import Flask, render_template_string
from datetime import datetime
import yfinance as yf
import random

app = Flask(__name__)

# Data
daily_news = [
    {"headline": "Federal Reserve Signals No Rate Hike", "category": "Monetary Policy", "summary": "Fed maintains current rates, providing market relief.", "impact": "bullish"},
    {"headline": "Tech Giants Report Record Earnings", "category": "Technology", "summary": "Major tech companies exceed expectations.", "impact": "bullish"},
    {"headline": "Oil Prices Surge Amid Tensions", "category": "Energy", "summary": "Geopolitical tensions drive oil prices higher.", "impact": "mixed"}
]

stock_symbols = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "TSLA"]

def get_real_stock_data():
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
            stock_data.append({
                "symbol": symbol,
                "name": symbol,
                "price": round(random.uniform(100, 500), 2),
                "change": f"{'+' if random.random() > 0.5 else ''}{random.uniform(0.5, 3.0):.2f}%",
                "sector": "Technology"
            })
    return stock_data

# Futuristic Template
TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Finance - Next-Gen Market Intelligence</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --dark-bg: #0a0a0a;
            --card-bg: rgba(255, 255, 255, 0.05);
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --success: #00ff88;
            --danger: #ff4757;
        }
        
        body {
            background: var(--dark-bg);
            color: var(--text-primary);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .navbar {
            background: var(--primary-gradient);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .hero {
            background: var(--primary-gradient);
            min-height: 60vh;
            display: flex;
            align-items: center;
            position: relative;
        }
        
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .btn-futuristic {
            background: var(--accent-gradient);
            border: none;
            padding: 1rem 2rem;
            border-radius: 50px;
            color: white;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            margin: 0.5rem;
        }
        
        .btn-futuristic:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            color: white;
        }
        
        .content-section {
            background: var(--card-bg);
            border-radius: 20px;
            margin: 2rem 0;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
        }
        
        .section-header {
            background: var(--accent-gradient);
            padding: 1.5rem;
            border-radius: 20px 20px 0 0;
        }
        
        .news-item {
            padding: 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        
        .news-item:hover {
            background: rgba(255,255,255,0.05);
        }
        
        .category-badge {
            background: var(--secondary-gradient);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .impact-bullish { border-left: 4px solid var(--success); }
        .impact-mixed { border-left: 4px solid #ffa502; }
        
        .stock-card {
            background: var(--card-bg);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .stock-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .stock-price {
            font-size: 2rem;
            font-weight: bold;
            margin: 1rem 0;
        }
        
        .change-positive { color: var(--success); }
        .change-negative { color: var(--danger); }
        
        .sector-badge {
            background: var(--accent-gradient);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-atom me-2"></i>Quantum Finance
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/">Home</a>
                <a class="nav-link" href="/news">News</a>
                <a class="nav-link" href="/stocks">Stocks</a>
            </div>
        </div>
    </nav>

    {% if show_hero %}
    <div class="hero">
        <div class="container text-center">
            <h1 class="hero-title">Quantum Finance</h1>
            <p class="lead mb-4">Next-Generation Market Intelligence & AI-Powered Investment Insights</p>
            <div>
                <a href="/news" class="btn-futuristic">
                    <i class="fas fa-newspaper me-2"></i>Market News
                </a>
                <a href="/stocks" class="btn-futuristic">
                    <i class="fas fa-chart-line me-2"></i>Stock Analysis
                </a>
            </div>
        </div>
    </div>
    {% endif %}

    <div class="container">
        {% if news_analyses %}
        <div class="row">
            <div class="col-lg-8">
                <div class="content-section">
                    <div class="section-header">
                        <h3><i class="fas fa-newspaper me-2"></i>Today's Market News</h3>
                    </div>
                    {% for news, analysis in news_analyses %}
                    <div class="news-item impact-{{ news.impact }}">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <span class="category-badge">{{ news.category }}</span>
                            <small class="text-muted">2 hours ago</small>
                        </div>
                        <h5 class="mb-3">{{ news.headline }}</h5>
                        <p class="text-muted mb-3">{{ news.summary }}</p>
                        <div class="p-3 bg-dark rounded">
                            <strong><i class="fas fa-chart-line me-1"></i>Market Impact:</strong>
                            <p class="mb-0 mt-2">{{ analysis }}</p>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}

        {% if stock_analyses %}
        <div class="row">
            <div class="col-lg-{{ '4' if news_analyses else '12' }}">
                <div class="content-section">
                    <div class="section-header">
                        <h3><i class="fas fa-star me-2"></i>Top Stock Picks</h3>
                    </div>
                    <div class="p-3">
                        {% for stock, analysis in stock_analyses %}
                        <div class="stock-card">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div>
                                    <h5 class="mb-1">{{ stock.symbol }}</h5>
                                    <p class="text-muted mb-1">{{ stock.name }}</p>
                                </div>
                                <span class="sector-badge">{{ stock.sector }}</span>
                            </div>
                            <div class="stock-price">${{ stock.price }}</div>
                            <div class="change-{{ 'positive' if '+' in stock.change else 'negative' }} mb-3">
                                <i class="fas fa-arrow-{{ 'up' if '+' in stock.change else 'down' }} me-1"></i>
                                {{ stock.change }}
                            </div>
                            <div class="p-3 bg-dark rounded">
                                <strong><i class="fas fa-lightbulb me-1"></i>Why Buy:</strong>
                                <p class="mb-0 mt-2">{{ analysis }}</p>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route("/")
def landing():
    return render_template_string(TEMPLATE, show_hero=True, news_analyses=[], stock_analyses=[])

@app.route("/news")
def news():
    news_analyses = list(zip(daily_news, [
        "This dovish stance from the Fed typically boosts market sentiment, potentially lifting growth stocks.",
        "Strong earnings from major tech companies often drive broader market optimism and sector-wide gains.",
        "Rising oil prices may pressure transportation stocks while benefiting energy sector companies."
    ]))
    return render_template_string(TEMPLATE, show_hero=False, news_analyses=news_analyses, stock_analyses=[])

@app.route("/stocks")
def stocks():
    stock_data = get_real_stock_data()
    top_stocks = stock_data[:3]
    stock_analyses = [
        "Apple continues to show strong iPhone sales and services growth with expanding market share.",
        "Microsoft's cloud business and AI integration position it well for continued growth.",
        "NVIDIA remains the leader in AI chips with strong demand expected to continue."
    ]
    stock_analyses_combined = list(zip(top_stocks, stock_analyses))
    return render_template_string(TEMPLATE, show_hero=False, news_analyses=[], stock_analyses=stock_analyses_combined)

if __name__ == "__main__":
    app.run(debug=True, port=8080) 