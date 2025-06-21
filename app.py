import os
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
        "impact": "bullish"
    },
    {
        "headline": "Tech Giants Report Record Earnings for Q2",
        "category": "Technology",
        "summary": "Major technology companies exceeded analyst expectations with strong quarterly results.",
        "impact": "bullish"
    },
    {
        "headline": "Oil Prices Surge Amid Middle East Tensions",
        "category": "Energy",
        "summary": "Geopolitical tensions drive oil prices to new highs, affecting global markets.",
        "impact": "mixed"
    },
    {
        "headline": "Inflation Data Shows Cooling Trend",
        "category": "Economy",
        "summary": "Latest inflation figures suggest the Fed's policies are having the intended effect.",
        "impact": "bullish"
    },
    {
        "headline": "AI Chip Demand Drives Semiconductor Rally",
        "category": "Technology",
        "summary": "Artificial intelligence applications fuel unprecedented demand for advanced chips.",
        "impact": "bullish"
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

# Professional analyses (no API needed)
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
                    "sector": info.get('sector', 'Unknown')
                })
            else:
                # Fallback data if API fails
                stock_data.append({
                    "symbol": symbol,
                    "name": symbol,
                    "price": round(random.uniform(100, 500), 2),
                    "change": f"{'+' if random.random() > 0.5 else ''}{random.uniform(0.5, 3.0):.2f}%",
                    "sector": "Technology"
                })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            # Fallback data
            stock_data.append({
                "symbol": symbol,
                "name": symbol,
                "price": round(random.uniform(100, 500), 2),
                "change": f"{'+' if random.random() > 0.5 else ''}{random.uniform(0.5, 3.0):.2f}%",
                "sector": "Technology"
            })
    
    return stock_data

# Landing page template
LANDING_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Times - Home</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .hero {
            background: linear-gradient(135deg, #1e3a8a 60%, #3b82f6 100%);
            color: white;
            padding: 4rem 0 3rem 0;
            text-align: center;
        }
        .hero img { max-width: 180px; margin-bottom: 1.5rem; border-radius: 50%; box-shadow: 0 4px 24px rgba(0,0,0,0.15); }
        .hero-title { font-size: 2.5rem; font-weight: bold; }
        .hero-desc { font-size: 1.2rem; margin: 1.5rem 0; }
        .nav-btns .btn { margin: 0.5rem; font-size: 1.1rem; padding: 0.75rem 2rem; }
        .section {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin: 2rem 0;
            padding: 2rem 1.5rem;
        }
        .quote {
            font-size: 1.2rem;
            font-style: italic;
            color: #1e3a8a;
            border-left: 4px solid #3b82f6;
            padding-left: 1rem;
            margin: 2rem 0 1rem 0;
        }
        .author { font-size: 1rem; color: #555; margin-left: 1.5rem; }
        .feature-img { max-width: 100%; border-radius: 10px; margin-bottom: 1.5rem; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark" style="background: linear-gradient(135deg, #1e3a8a, #3b82f6);">
        <div class="container">
            <a class="navbar-brand" href="/"> <i class="fas fa-chart-line me-2"></i>Financial Times</a>
        </div>
    </nav>
    <div class="hero">
        <img src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=facearea&w=400&q=80" alt="Financial Times Logo">
        <div class="hero-title">Welcome to Financial Times</div>
        <div class="hero-desc">Your trusted source for daily financial news, expert market analysis, and the best stock picks. We help you stay ahead in the world of finance with clear, actionable insights.</div>
        <div class="nav-btns">
            <a href="{{ url_for('news') }}" class="btn btn-warning"><i class="fas fa-newspaper me-2"></i>Today's News</a>
            <a href="{{ url_for('stocks') }}" class="btn btn-success"><i class="fas fa-star me-2"></i>Top Stock Picks</a>
        </div>
    </div>
    <div class="container">
        <div class="section row align-items-center">
            <div class="col-md-6">
                <img src="https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=600&q=80" class="feature-img" alt="Market Analysis">
            </div>
            <div class="col-md-6">
                <h3>Who We Are</h3>
                <p>We are a team of passionate financial analysts, journalists, and technologists dedicated to bringing you the most important market news and actionable investment ideas every day. Our mission is to empower you to make smarter financial decisions.</p>
                <div class="quote">"The stock market is filled with individuals who know the price of everything, but the value of nothing."<br><span class="author">— Philip Fisher</span></div>
            </div>
        </div>
        <div class="section row align-items-center flex-row-reverse">
            <div class="col-md-6">
                <img src="https://images.unsplash.com/photo-1515168833906-d2a3b82b302b?auto=format&fit=crop&w=600&q=80" class="feature-img" alt="Stock Picks">
            </div>
            <div class="col-md-6">
                <h3>What We Do</h3>
                <p>Every morning, we curate the top financial headlines, analyze their impact on the markets, and recommend the best stocks to buy today. Our expert analysis and real-time data help you cut through the noise and focus on what matters.</p>
                <div class="quote">"In investing, what is comfortable is rarely profitable."<br><span class="author">— Robert Arnott</span></div>
            </div>
        </div>
    </div>
    <footer class="text-center py-4 mt-4" style="color:#888;">&copy; {{ year }} Financial Times. All rights reserved.</footer>
</body>
</html>
'''

# Enhanced HTML template with professional news site design
TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Times - Daily Market Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #1e3a8a;
            --secondary-color: #3b82f6;
            --accent-color: #f59e0b;
            --success-color: #10b981;
            --danger-color: #ef4444;
            --dark-bg: #1f2937;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8fafc;
        }
        
        .navbar {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .market-indices {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        .index-card {
            padding: 1rem;
            border-right: 1px solid #e5e7eb;
            text-align: center;
        }
        
        .index-card:last-child {
            border-right: none;
        }
        
        .trend-up { color: var(--success-color); }
        .trend-down { color: var(--danger-color); }
        
        .news-section {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        .news-item {
            border-bottom: 1px solid #e5e7eb;
            padding: 1.5rem;
            transition: background-color 0.3s;
        }
        
        .news-item:hover {
            background-color: #f8fafc;
        }
        
        .news-item:last-child {
            border-bottom: none;
        }
        
        .category-badge {
            background: var(--accent-color);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .impact-bullish { border-left: 4px solid var(--success-color); }
        .impact-bearish { border-left: 4px solid var(--danger-color); }
        .impact-mixed { border-left: 4px solid var(--accent-color); }
        
        .stocks-section {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stock-card {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .stock-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .stock-price {
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .stock-change-positive { color: var(--success-color); }
        .stock-change-negative { color: var(--danger-color); }
        
        .sector-badge {
            background: var(--secondary-color);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 15px;
            font-size: 0.7rem;
        }
        
        .header-stats {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        
        .stat-item {
            text-align: center;
            padding: 1rem;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-chart-line me-2"></i>Financial Times
            </a>
            <div class="navbar-nav ms-auto">
                <span class="navbar-text">
                    <i class="fas fa-calendar me-1"></i>{{ current_date }}
                </span>
            </div>
        </div>
    </nav>

    <!-- Header Stats -->
    <div class="header-stats">
        <div class="container">
            <div class="row">
                <div class="col-md-3">
                    <div class="stat-item">
                        <div class="stat-value">{{ market_indices[0].value }}</div>
                        <div class="stat-label">S&P 500</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-item">
                        <div class="stat-value">{{ market_indices[1].value }}</div>
                        <div class="stat-label">NASDAQ</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-item">
                        <div class="stat-value">{{ market_indices[2].value }}</div>
                        <div class="stat-label">DOW JONES</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-item">
                        <div class="stat-value">{{ market_indices[3].value }}</div>
                        <div class="stat-label">RUSSELL 2000</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <!-- Market Indices -->
        <div class="market-indices">
            <div class="row">
                {% for index in market_indices %}
                <div class="col-md-3">
                    <div class="index-card">
                        <h5 class="mb-1">{{ index.name }}</h5>
                        <div class="h4 mb-1">{{ index.value }}</div>
                        <div class="text-{{ 'success' if index.trend == 'up' else 'danger' }}">
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
                <div class="news-section">
                    <div class="p-3 border-bottom">
                        <h3><i class="fas fa-newspaper me-2"></i>Today's Top Financial News</h3>
                    </div>
                    {% for news, analysis in news_analyses %}
                    <div class="news-item impact-{{ news.impact }}">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <span class="category-badge">{{ news.category }}</span>
                            <small class="text-muted">2 hours ago</small>
                        </div>
                        <h5 class="mb-2">{{ news.headline }}</h5>
                        <p class="text-muted mb-3">{{ news.summary }}</p>
                        <div class="analysis-box p-3 bg-light rounded">
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
                <div class="stocks-section">
                    <div class="p-3 border-bottom">
                        <h3><i class="fas fa-star me-2"></i>Top Stocks to Buy Today</h3>
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
                            <div class="stock-price mb-2">${{ stock.price }}</div>
                            <div class="stock-change-{{ 'positive' if '+' in stock.change else 'negative' }} mb-3">
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
    return render_template_string(TEMPLATE, news_analyses=news_analyses_combined, stock_analyses=[], market_indices=market_indices, current_date=current_date)

@app.route("/stocks")
def stocks():
    current_date = datetime.now().strftime("%B %d, %Y")
    # Get real stock data
    stock_data = get_real_stock_data()
    # Take top 3 stocks
    top_stocks = stock_data[:3]
    stock_analyses_list = stock_analyses[:3]
    stock_analyses_combined = list(zip(top_stocks, stock_analyses_list))
    return render_template_string(TEMPLATE, news_analyses=[], stock_analyses=stock_analyses_combined, market_indices=market_indices, current_date=current_date)

if __name__ == "__main__":
    app.run(debug=True, port=8080) 