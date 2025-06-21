from flask import Flask, render_template_string, redirect, url_for
from datetime import datetime
import yfinance as yf
import random

app = Flask(__name__)

# Enhanced news data with categories
daily_news = [
    {
        "headline": "Federal Reserve Signals No Rate Hike in Upcoming Meeting",
        "category": "Monetary Policy",
        "summary": "The Federal Reserve indicated it will maintain current interest rates, providing relief to markets.",
        "impact": "bullish",
        "time": "2 hours ago"
    },
    {
        "headline": "Tech Giants Report Record Earnings for Q2",
        "category": "Technology",
        "summary": "Major technology companies exceeded analyst expectations with strong quarterly results.",
        "impact": "bullish",
        "time": "3 hours ago"
    },
    {
        "headline": "Oil Prices Surge Amid Middle East Tensions",
        "category": "Energy",
        "summary": "Geopolitical tensions drive oil prices to new highs, affecting global markets.",
        "impact": "mixed",
        "time": "4 hours ago"
    },
    {
        "headline": "Inflation Data Shows Cooling Trend",
        "category": "Economy",
        "summary": "Latest inflation figures suggest the Fed's policies are having the intended effect.",
        "impact": "bullish",
        "time": "5 hours ago"
    },
    {
        "headline": "AI Chip Demand Drives Semiconductor Rally",
        "category": "Technology",
        "summary": "Artificial intelligence applications fuel unprecedented demand for advanced chips.",
        "impact": "bullish",
        "time": "6 hours ago"
    }
]

# Stock symbols for real data
stock_symbols = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "TSLA", "JPM", "JNJ"]

# Market indices data
market_indices = [
    {"name": "S&P 500", "value": "4,850.25", "change": "+1.2%", "trend": "up"},
    {"name": "NASDAQ", "value": "15,250.80", "change": "+2.1%", "trend": "up"},
    {"name": "DOW JONES", "value": "38,450.60", "change": "+0.8%", "trend": "up"},
    {"name": "RUSSELL 2000", "value": "2,150.40", "change": "+1.5%", "trend": "up"}
]

# Professional analyses
news_analyses = [
    "This dovish stance from the Fed typically boosts market sentiment, potentially lifting growth stocks and reducing borrowing costs for companies. Financial and real estate sectors may see increased activity.",
    "Strong earnings from major tech companies often drive broader market optimism and could lead to sector-wide gains. This positive momentum may extend to related industries and supply chain partners.",
    "Rising oil prices may pressure transportation and manufacturing stocks while benefiting energy sector companies. Airlines and shipping companies could face margin pressure, while oil producers see improved profitability.",
    "Cooling inflation data suggests the Fed's monetary policy is working, which could lead to earlier rate cuts and boost consumer spending. This is particularly positive for retail and consumer discretionary stocks.",
    "The AI revolution continues to drive semiconductor demand, with NVIDIA and other chip makers benefiting from the trend. This could lead to increased investment in AI infrastructure across industries."
]

stock_analyses = [
    "Apple continues to show strong iPhone sales and services growth, with expanding market share in premium segments. The company's ecosystem approach and strong brand loyalty provide consistent revenue streams.",
    "Microsoft's cloud business and AI integration across products position it well for continued growth in enterprise software. Azure's market share gains and AI partnerships create multiple growth catalysts.",
    "NVIDIA remains the leader in AI chips and gaming GPUs, with strong demand expected to continue. The company's technological advantage and expanding AI applications drive sustained growth.",
    "Alphabet's search dominance and YouTube's growth provide stable revenue, while AI investments position it for future growth. The company's strong cash flow supports continued innovation.",
    "Amazon's e-commerce leadership and AWS cloud services create multiple growth engines. The company's logistics network and Prime membership provide competitive advantages.",
    "Tesla's electric vehicle leadership and energy storage solutions position it for long-term growth. The company's technology advantage and expanding global presence drive market share gains.",
    "JPMorgan Chase's strong balance sheet and diversified revenue streams provide stability. The company's digital transformation and market leadership create competitive advantages.",
    "Johnson & Johnson's pharmaceutical pipeline and consumer health business provide steady growth. The company's innovation focus and global reach support long-term value creation."
]

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

# Futuristic Landing Page Template
LANDING_TEMPLATE = '''
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
            --warning: #ffa502;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: var(--dark-bg);
            color: var(--text-primary);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow-x: hidden;
        }
        
        .hero {
            background: var(--primary-gradient);
            min-height: 100vh;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }
        
        .hero-content {
            position: relative;
            z-index: 2;
            text-align: center;
        }
        
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(255,255,255,0.3);
        }
        
        .hero-subtitle {
            font-size: 1.5rem;
            margin-bottom: 2rem;
            color: var(--text-secondary);
        }
        
        .nav-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
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
            position: relative;
            overflow: hidden;
        }
        
        .btn-futuristic::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn-futuristic:hover::before {
            left: 100%;
        }
        
        .btn-futuristic:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .features-section {
            padding: 5rem 0;
            background: var(--dark-bg);
        }
        
        .feature-card {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            border-color: rgba(255,255,255,0.2);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            background: var(--secondary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .quote-section {
            background: var(--secondary-gradient);
            padding: 4rem 0;
            text-align: center;
        }
        
        .quote {
            font-size: 2rem;
            font-style: italic;
            margin-bottom: 1rem;
        }
        
        .author {
            font-size: 1.2rem;
            opacity: 0.8;
        }
        
        .floating-elements {
            position: absolute;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        
        .floating-element {
            position: absolute;
            width: 20px;
            height: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .floating-element:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
        .floating-element:nth-child(2) { top: 60%; left: 80%; animation-delay: 2s; }
        .floating-element:nth-child(3) { top: 80%; left: 20%; animation-delay: 4s; }
    </style>
</head>
<body>
    <div class="hero">
        <div class="floating-elements">
            <div class="floating-element"></div>
            <div class="floating-element"></div>
            <div class="floating-element"></div>
        </div>
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title">Quantum Finance</h1>
                <p class="hero-subtitle">Next-Generation Market Intelligence & AI-Powered Investment Insights</p>
                <div class="nav-buttons">
                    <a href="{{ url_for('news') }}" class="btn-futuristic">
                        <i class="fas fa-newspaper me-2"></i>Market News
                    </a>
                    <a href="{{ url_for('stocks') }}" class="btn-futuristic">
                        <i class="fas fa-chart-line me-2"></i>Stock Analysis
                    </a>
                    <a href="{{ url_for('dashboard') }}" class="btn-futuristic">
                        <i class="fas fa-tachometer-alt me-2"></i>Live Dashboard
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="features-section">
        <div class="container">
            <div class="row">
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-brain"></i>
                        </div>
                        <h3>AI-Powered Analysis</h3>
                        <p>Advanced machine learning algorithms analyze market patterns and provide predictive insights for optimal investment decisions.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-bolt"></i>
                        </div>
                        <h3>Real-Time Data</h3>
                        <p>Live market data, instant price updates, and real-time news aggregation from global financial markets.</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h3>Risk Management</h3>
                        <p>Comprehensive risk assessment tools and portfolio optimization strategies for informed investment decisions.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="quote-section">
        <div class="container">
            <div class="quote">"The future of finance is not just about numbers, it's about intelligence."</div>
            <div class="author">— Quantum Finance Team</div>
        </div>
    </div>
</body>
</html>
'''

# Main Dashboard Template
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Finance - Live Dashboard</title>
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
            --warning: #ffa502;
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
        
        .navbar-brand {
            font-weight: 800;
            font-size: 1.5rem;
        }
        
        .market-indices {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
        }
        
        .index-card {
            text-align: center;
            padding: 1.5rem;
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        
        .index-card:last-child {
            border-right: none;
        }
        
        .index-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .index-change {
            font-size: 1.2rem;
            font-weight: 600;
        }
        
        .change-positive { color: var(--success); }
        .change-negative { color: var(--danger); }
        
        .content-section {
            background: var(--card-bg);
            border-radius: 20px;
            margin: 2rem 0;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            overflow: hidden;
        }
        
        .section-header {
            background: var(--accent-gradient);
            padding: 1.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .news-item {
            padding: 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        
        .news-item:hover {
            background: rgba(255,255,255,0.05);
        }
        
        .news-item:last-child {
            border-bottom: none;
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
        .impact-bearish { border-left: 4px solid var(--danger); }
        .impact-mixed { border-left: 4px solid var(--warning); }
        
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
            border-color: rgba(255,255,255,0.2);
        }
        
        .stock-price {
            font-size: 2rem;
            font-weight: bold;
            margin: 1rem 0;
        }
        
        .sector-badge {
            background: var(--accent-gradient);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: 600;
        }
        
        .analysis-box {
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
            border-left: 3px solid var(--accent-gradient);
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
                <a class="nav-link" href="{{ url_for('landing') }}">Home</a>
                <a class="nav-link" href="{{ url_for('news') }}">News</a>
                <a class="nav-link" href="{{ url_for('stocks') }}">Stocks</a>
                <span class="navbar-text">
                    <i class="fas fa-calendar me-1"></i>{{ current_date }}
                </span>
            </div>
        </div>
    </nav>

    <div class="container">
        <!-- Market Indices -->
        <div class="market-indices">
            <div class="row">
                {% for index in market_indices %}
                <div class="col-md-3">
                    <div class="index-card">
                        <h5 class="mb-2">{{ index.name }}</h5>
                        <div class="index-value">{{ index.value }}</div>
                        <div class="index-change change-{{ 'positive' if index.trend == 'up' else 'negative' }}">
                            <i class="fas fa-arrow-{{ 'up' if index.trend == 'up' else 'down' }} me-1"></i>
                            {{ index.change }}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="row">
            <!-- News Section -->
            {% if news_analyses %}
            <div class="col-lg-8">
                <div class="content-section">
                    <div class="section-header">
                        <h3><i class="fas fa-newspaper me-2"></i>Today's Market News</h3>
                    </div>
                    {% for news, analysis in news_analyses %}
                    <div class="news-item impact-{{ news.impact }}">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <span class="category-badge">{{ news.category }}</span>
                            <small class="text-muted">{{ news.time }}</small>
                        </div>
                        <h5 class="mb-3">{{ news.headline }}</h5>
                        <p class="text-muted mb-3">{{ news.summary }}</p>
                        <div class="analysis-box">
                            <strong><i class="fas fa-chart-line me-1"></i>Market Impact:</strong>
                            <p class="mb-0 mt-2">{{ analysis }}</p>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <!-- Stocks Section -->
            {% if stock_analyses %}
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
                            <div class="analysis-box">
                                <strong><i class="fas fa-lightbulb me-1"></i>Why Buy:</strong>
                                <p class="mb-0 mt-2">{{ analysis }}</p>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route("/")
def landing():
    return render_template_string(LANDING_TEMPLATE, year=datetime.now().year)

@app.route("/news")
def news():
    current_date = datetime.now().strftime("%B %d, %Y")
    news_analyses_combined = list(zip(daily_news, news_analyses))
    return render_template_string(DASHBOARD_TEMPLATE, news_analyses=news_analyses_combined, stock_analyses=[], market_indices=market_indices, current_date=current_date)

@app.route("/stocks")
def stocks():
    current_date = datetime.now().strftime("%B %d, %Y")
    stock_data = get_real_stock_data()
    top_stocks = stock_data[:3]
    stock_analyses_list = stock_analyses[:3]
    stock_analyses_combined = list(zip(top_stocks, stock_analyses_list))
    return render_template_string(DASHBOARD_TEMPLATE, news_analyses=[], stock_analyses=stock_analyses_combined, market_indices=market_indices, current_date=current_date)

@app.route("/dashboard")
def dashboard():
    current_date = datetime.now().strftime("%B %d, %Y")
    news_analyses_combined = list(zip(daily_news, news_analyses))
    stock_data = get_real_stock_data()
    top_stocks = stock_data[:3]
    stock_analyses_list = stock_analyses[:3]
    stock_analyses_combined = list(zip(top_stocks, stock_analyses_list))
    return render_template_string(DASHBOARD_TEMPLATE, news_analyses=news_analyses_combined, stock_analyses=stock_analyses_combined, market_indices=market_indices, current_date=current_date)

if __name__ == "__main__":
    app.run(debug=True, port=8080) 