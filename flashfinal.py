from flask import Flask, render_template_string, redirect, url_for, request, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np

app = Flask(__name__)

# PULSE - Professional Financial Intelligence Platform
# Logo: Minimalist black and white design with clean typography

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

def get_live_stock_data(symbol):
    """Get live stock data including price, change, and percentage change"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="2d")
        if len(hist) >= 2:
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2]
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
            return {
                'price': round(current_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'success': True
            }
        else:
            return {'success': False, 'price': 0, 'change': 0, 'change_percent': 0}
    except Exception as e:
        print(f"Error fetching live data for {symbol}: {e}")
        return {'success': False, 'price': 0, 'change': 0, 'change_percent': 0}

def get_stock_chart_data(symbol, period="6mo"):
    """Get stock data for charts with technical indicators"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        
        if hist.empty:
            return None
            
        # Calculate technical indicators
        # RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
        exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        
        # Moving Averages
        ma20 = hist['Close'].rolling(window=20).mean()
        ma50 = hist['Close'].rolling(window=50).mean()
        ma200 = hist['Close'].rolling(window=200).mean()
        
        # Prepare chart data
        chart_data = []
        for i, (date, row) in enumerate(hist.iterrows()):
            chart_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close']),
                'volume': int(row['Volume']),
                'rsi': float(rsi.iloc[i]) if not pd.isna(rsi.iloc[i]) else None,
                'macd': float(macd.iloc[i]) if not pd.isna(macd.iloc[i]) else None,
                'signal': float(signal.iloc[i]) if not pd.isna(signal.iloc[i]) else None,
                'ma20': float(ma20.iloc[i]) if not pd.isna(ma20.iloc[i]) else None,
                'ma50': float(ma50.iloc[i]) if not pd.isna(ma50.iloc[i]) else None,
                'ma200': float(ma200.iloc[i]) if not pd.isna(ma200.iloc[i]) else None
            })
        
        return chart_data
    except Exception as e:
        print(f"Error fetching chart data for {symbol}: {e}")
        return None

def get_portfolio_performance(symbols):
    """Get performance comparison for multiple stocks"""
    performance_data = []
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1mo")
            if not hist.empty:
                start_price = hist['Close'].iloc[0]
                end_price = hist['Close'].iloc[-1]
                change = end_price - start_price
                change_percent = (change / start_price) * 100
                
                performance_data.append({
                    'symbol': symbol,
                    'start_price': round(start_price, 2),
                    'end_price': round(end_price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'success': True
                })
            else:
                performance_data.append({
                    'symbol': symbol,
                    'success': False
                })
        except Exception as e:
            performance_data.append({
                'symbol': symbol,
                'success': False
            })
    
    return performance_data

# Sample portfolios (in a real app, this would be stored in a database)
sample_portfolios = {
    'tech_portfolio': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA'],
    'growth_portfolio': ['TSLA', 'NFLX', 'META', 'CRM', 'ADBE'],
    'value_portfolio': ['JNJ', 'PG', 'KO', 'WMT', 'JPM']
}

# Emerging opportunities - high-potential stocks with strong fundamentals
emerging_opportunities = [
    {
        'symbol': 'CRWD',
        'name': 'CrowdStrike Holdings',
        'sector': 'Cybersecurity',
        'reason': 'Leading cloud-native cybersecurity platform with exceptional growth in endpoint protection and threat intelligence',
        'recommendation': 'STRONG BUY',
        'target': '$320',
        'analysis': 'Exceptional revenue growth (35% YoY), expanding enterprise customer base, and technological leadership in AI-powered security. Cloud-native architecture provides significant competitive advantages.'
    },
    {
        'symbol': 'PLTR',
        'name': 'Palantir Technologies',
        'sector': 'Data Analytics & AI',
        'reason': 'Advanced AI-powered data analytics platform serving government and enterprise with unique artificial intelligence capabilities',
        'recommendation': 'BUY',
        'target': '$28',
        'analysis': 'Government contracts provide stable revenue foundation, AI platform expansion accelerating, and growing commercial adoption. Strong competitive moat in data analytics space.'
    },
    {
        'symbol': 'NET',
        'name': 'Cloudflare',
        'sector': 'Cloud Infrastructure',
        'reason': 'Web security and performance optimization leader with global CDN network and zero-trust security solutions',
        'recommendation': 'BUY',
        'target': '$135',
        'analysis': 'Zero-trust security growth accelerating, edge computing expansion, and strong enterprise adoption. Network effects create significant barriers to entry.'
    },
    {
        'symbol': 'ZM',
        'name': 'Zoom Video Communications',
        'sector': 'Communication Technology',
        'reason': 'Video conferencing market leader with enterprise growth and AI integration capabilities',
        'recommendation': 'HOLD',
        'target': '$80',
        'analysis': 'Post-pandemic normalization phase, but strong enterprise features and AI capabilities. Competition from Microsoft Teams remains significant.'
    },
    {
        'symbol': 'SNOW',
        'name': 'Snowflake',
        'sector': 'Cloud Data Platform',
        'reason': 'Cloud-native data platform with exceptional scalability and data warehousing capabilities',
        'recommendation': 'BUY',
        'target': '$180',
        'analysis': 'Strong product-market fit, expanding customer base, and leadership in cloud data warehousing. High switching costs create customer retention.'
    },
    {
        'symbol': 'PATH',
        'name': 'UiPath',
        'sector': 'Robotic Process Automation',
        'reason': 'Leading RPA platform with AI-powered automation solutions for enterprise efficiency',
        'recommendation': 'BUY',
        'target': '$25',
        'analysis': 'RPA market growth, AI integration, and enterprise automation demand. Strong competitive position in automation space.'
    }
]

# Risk assessment - stocks requiring careful evaluation
risk_assessment_stocks = [
    {
        'symbol': 'NFLX',
        'name': 'Netflix',
        'sector': 'Entertainment',
        'reason': 'Streaming market saturation and increasing competition from major players',
        'recommendation': 'SELL',
        'target': '$350',
        'analysis': 'Market saturation concerns, password sharing crackdown impact, and intensifying competition from Disney+, HBO Max, and others. Subscriber growth slowing.'
    },
    {
        'symbol': 'UBER',
        'name': 'Uber Technologies',
        'sector': 'Transportation',
        'reason': 'Regulatory challenges and profitability concerns in core ride-sharing business',
        'recommendation': 'HOLD',
        'target': '$45',
        'analysis': 'Regulatory headwinds, driver shortage issues, and path to profitability remains uncertain. Diversification into delivery provides some offset.'
    },
    {
        'symbol': 'LYFT',
        'name': 'Lyft',
        'sector': 'Transportation',
        'reason': 'Market share loss to Uber and similar regulatory challenges',
        'recommendation': 'SELL',
        'target': '$12',
        'analysis': 'Losing market share to Uber, regulatory challenges, and limited international presence. Profitability timeline uncertain.'
    },
    {
        'symbol': 'PINS',
        'name': 'Pinterest',
        'sector': 'Social Media',
        'reason': 'User growth plateau and advertising market challenges',
        'recommendation': 'HOLD',
        'target': '$28',
        'analysis': 'User growth slowing, advertising market headwinds, and competition from larger social platforms. Monetization improvements needed.'
    },
    {
        'symbol': 'SNAP',
        'name': 'Snap',
        'sector': 'Social Media',
        'reason': 'Advertising market pressure and user engagement challenges',
        'recommendation': 'SELL',
        'target': '$8',
        'analysis': 'Apple privacy changes impact, advertising market pressure, and competition from Meta platforms. Path to profitability unclear.'
    },
    {
        'symbol': 'ROKU',
        'name': 'Roku',
        'sector': 'Streaming',
        'reason': 'Platform competition and advertising market challenges',
        'recommendation': 'HOLD',
        'target': '$65',
        'analysis': 'Smart TV competition, advertising market pressure, and content platform challenges. Hardware margins under pressure.'
    }
]

# Market indices
market_indices = [
    {'symbol': '^GSPC', 'name': 'S&P 500'},
    {'symbol': '^DJI', 'name': 'Dow Jones'},
    {'symbol': '^IXIC', 'name': 'NASDAQ'},
    {'symbol': '^VIX', 'name': 'VIX'}
]

# Financial news
financial_news = [
    {
        'title': 'Federal Reserve Signals Potential Rate Cuts in 2024',
        'summary': 'The Fed indicates possible monetary policy easing as inflation shows signs of cooling. Markets react positively to dovish signals.',
        'impact': 'BULLISH - Lower rates typically boost stock markets and growth stocks',
        'time': '2 hours ago',
        'details': 'Fed Chair Powell suggests inflation is moving toward target, opening door for rate cuts. Bond yields decline, tech stocks rally.'
    },
    {
        'title': 'Tech Sector Earnings Beat Expectations',
        'summary': 'Major technology companies report stronger-than-expected quarterly results, driven by AI investments and cloud growth.',
        'impact': 'BULLISH - Strong earnings support market valuations and tech sector leadership',
        'time': '4 hours ago',
        'details': 'Microsoft, Alphabet, and Amazon all beat estimates. AI revenue growth accelerating across major tech companies.'
    },
    {
        'title': 'Oil Prices Surge on Supply Concerns',
        'summary': 'Geopolitical tensions and supply disruptions drive oil prices higher, impacting inflation and energy stocks.',
        'impact': 'MIXED - Energy stocks benefit, but inflation concerns rise',
        'time': '6 hours ago',
        'details': 'Middle East tensions and OPEC+ production cuts push oil above $85. Energy sector outperforms while inflation fears grow.'
    },
    {
        'title': 'Cryptocurrency Market Shows Volatility',
        'summary': 'Bitcoin and other cryptocurrencies experience significant price swings amid regulatory news and market sentiment shifts.',
        'impact': 'NEUTRAL - Increased volatility in crypto markets',
        'time': '8 hours ago',
        'details': 'Bitcoin fluctuates between $65K-$70K. SEC approval of spot ETFs provides support, but regulatory uncertainty remains.'
    },
    {
        'title': 'Housing Market Shows Signs of Recovery',
        'summary': 'Mortgage rates decline and home sales increase in key markets, supporting economic growth outlook.',
        'impact': 'BULLISH - Housing sector recovery supports economic growth',
        'time': '10 hours ago',
        'details': '30-year mortgage rates fall to 6.5%. Homebuilder stocks rally on improved affordability and demand.'
    },
    {
        'title': 'Retail Sales Beat Expectations',
        'summary': 'Consumer spending remains strong despite inflation, supporting economic growth and retail sector performance.',
        'impact': 'BULLISH - Strong consumer spending supports economic growth',
        'time': '12 hours ago',
        'details': 'Retail sales up 0.7% month-over-month. Consumer confidence improving, supporting discretionary spending.'
    },
    {
        'title': 'Manufacturing PMI Shows Expansion',
        'summary': 'ISM Manufacturing Index indicates sector expansion, supporting economic growth and industrial stocks.',
        'impact': 'BULLISH - Manufacturing growth supports economic expansion',
        'time': '14 hours ago',
        'details': 'PMI reading of 52.3 indicates expansion. Supply chain improvements and new orders growth driving optimism.'
    },
    {
        'title': 'Bank Earnings Mixed Amid Rate Environment',
        'summary': 'Major banks report mixed quarterly results as net interest margins stabilize and loan growth varies.',
        'impact': 'NEUTRAL - Mixed results across banking sector',
        'time': '16 hours ago',
        'details': 'JPMorgan and Bank of America beat estimates, while Wells Fargo misses. Credit quality remains strong.'
    }
]

@app.route('/')
def home():
    # Get live data for featured stocks
    featured_stocks = []
    for stock in emerging_opportunities[:6]:  # Show first 6 stocks on homepage
        live_data = get_live_stock_data(stock['symbol'])
        stock_with_data = stock.copy()
        if live_data['success']:
            stock_with_data['current_price'] = f"${live_data['price']}"
            stock_with_data['change'] = live_data['change']
            stock_with_data['change_percent'] = live_data['change_percent']
            stock_with_data['price_color'] = 'text-success' if live_data['change'] >= 0 else 'text-danger'
        else:
            stock_with_data['current_price'] = 'N/A'
            stock_with_data['change'] = 0
            stock_with_data['change_percent'] = 0
            stock_with_data['price_color'] = 'text-muted'
        featured_stocks.append(stock_with_data)
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PULSE - Professional Financial Intelligence Platform</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { 
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #000 100%); 
                color: #fff; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6;
            }
            .hero { 
                background: linear-gradient(135deg, rgba(0,0,0,0.8) 0%, rgba(26,26,26,0.9) 100%); 
                padding: 120px 0 80px; 
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
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
                opacity: 0.5;
            }
            .card { 
                background: rgba(255,255,255,0.03); 
                border: 1px solid rgba(255,255,255,0.1); 
                border-radius: 20px; 
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                border-color: rgba(255,255,255,0.2);
            }
            .stock-card { 
                background: rgba(255,255,255,0.05); 
                border: 1px solid rgba(255,255,255,0.1); 
                border-radius: 15px; 
                padding: 25px; 
                margin-bottom: 20px; 
                transition: all 0.3s ease;
            }
            .stock-card:hover {
                background: rgba(255,255,255,0.08);
                border-color: rgba(255,255,255,0.2);
            }
            .btn-primary { 
                background: linear-gradient(45deg, #fff, #f0f0f0); 
                color: #000; 
                border: none; 
                border-radius: 30px; 
                padding: 15px 35px; 
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            }
            .btn-outline-light { 
                border: 2px solid rgba(255,255,255,0.3); 
                border-radius: 30px; 
                padding: 15px 35px; 
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .btn-outline-light:hover {
                background: rgba(255,255,255,0.1);
                border-color: rgba(255,255,255,0.5);
                transform: translateY(-2px);
            }
            .navbar { 
                background: rgba(0,0,0,0.95) !important; 
                backdrop-filter: blur(20px); 
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .logo { 
                font-size: 2.2rem; 
                font-weight: 800; 
                background: linear-gradient(45deg, #fff, #ccc); 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                letter-spacing: 2px;
            }
            .feature-icon {
                font-size: 3rem;
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1rem;
            }
            .stats-card {
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                transition: all 0.3s ease;
            }
            .stats-card:hover {
                background: rgba(255,255,255,0.05);
                transform: translateY(-3px);
            }
            .gradient-text {
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            .section-title {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
            }
            .section-subtitle {
                font-size: 1.2rem;
                color: rgba(255,255,255,0.7);
                margin-bottom: 3rem;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
            <div class="container">
                <a class="navbar-brand logo" href="/">
                    <i class="fas fa-chart-line me-2"></i>PULSE
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="{{ url_for('market_pulse') }}">Market Intelligence</a>
                    <a class="nav-link" href="{{ url_for('underrated_stocks_page') }}">Emerging Opportunities</a>
                    <a class="nav-link" href="{{ url_for('stocks_to_sell_page') }}">Risk Assessment</a>
                    <a class="nav-link" href="{{ url_for('market_news') }}">Market Analysis</a>
                    <a class="nav-link" href="{{ url_for('portfolio_tracker') }}">Portfolio Management</a>
                    <a class="nav-link" href="{{ url_for('performance_comparison') }}">Performance Analytics</a>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="hero">
            <div class="container text-center position-relative">
                <h1 class="display-2 mb-4 gradient-text">Professional Financial Intelligence</h1>
                <p class="lead mb-5" style="font-size: 1.4rem; color: rgba(255,255,255,0.8);">
                    Advanced market analysis, emerging opportunity identification, and comprehensive portfolio management
                </p>
                <div class="d-flex justify-content-center gap-4 flex-wrap mb-5">
                    <a href="{{ url_for('market_pulse') }}" class="btn btn-primary btn-lg">
                        <i class="fas fa-chart-bar me-2"></i>Market Intelligence
                    </a>
                    <a href="{{ url_for('underrated_stocks_page') }}" class="btn btn-outline-light btn-lg">
                        <i class="fas fa-rocket me-2"></i>Emerging Opportunities
                    </a>
                    <a href="{{ url_for('portfolio_tracker') }}" class="btn btn-outline-light btn-lg">
                        <i class="fas fa-chart-line me-2"></i>Portfolio Management
                    </a>
                </div>
                
                <!-- Key Statistics -->
                <div class="row justify-content-center mt-5">
                    <div class="col-md-3 col-6 mb-3">
                        <div class="stats-card">
                            <div class="h3 gradient-text">500+</div>
                            <small class="text-muted">Stocks Analyzed</small>
                        </div>
                    </div>
                    <div class="col-md-3 col-6 mb-3">
                        <div class="stats-card">
                            <div class="h3 gradient-text">24/7</div>
                            <small class="text-muted">Real-time Data</small>
                        </div>
                    </div>
                    <div class="col-md-3 col-6 mb-3">
                        <div class="stats-card">
                            <div class="h3 gradient-text">95%</div>
                            <small class="text-muted">Accuracy Rate</small>
                        </div>
                    </div>
                    <div class="col-md-3 col-6 mb-3">
                        <div class="stats-card">
                            <div class="h3 gradient-text">50K+</div>
                            <small class="text-muted">Active Users</small>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Market Dashboard -->
        <section class="py-5">
            <div class="container">
                <div class="text-center mb-5">
                    <h2 class="section-title">Live Market Dashboard</h2>
                    <p class="section-subtitle">Real-time market data and emerging opportunity tracking</p>
                </div>
                <div class="row">
                    <div class="col-lg-8">
                        <div class="card p-4">
                            <h4 class="mb-4 gradient-text">Featured Emerging Opportunities</h4>
                            <div class="row">
                                {% for stock in featured_stocks %}
                                <div class="col-md-6 mb-3">
                                    <div class="stock-card">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <div>
                                                <h6 class="mb-1 fw-bold">{{ stock.symbol }}</h6>
                                                <small class="text-muted">{{ stock.name }}</small>
                                            </div>
                                            <div class="text-end">
                                                <div class="h6 mb-1 {{ stock.price_color }} fw-bold">{{ stock.current_price }}</div>
                                                <small class="{{ stock.price_color }}">
                                                    {% if stock.change >= 0 %}+{% endif %}{{ stock.change }} ({% if stock.change_percent >= 0 %}+{% endif %}{{ stock.change_percent }}%)
                                                </small>
                                            </div>
                                        </div>
                                        <div class="mt-3">
                                            <span class="badge bg-success me-2">{{ stock.recommendation }}</span>
                                            <span class="badge bg-warning me-2">Target: {{ stock.target }}</span>
                                            <a href="/charts/{{ stock.symbol }}" class="btn btn-sm btn-outline-light">Technical Analysis</a>
                                        </div>
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="card p-4">
                            <h4 class="mb-4 gradient-text">Market Indices</h4>
                            <div id="market-indices">
                                <div class="stock-card">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1 fw-bold">S&P 500</h6>
                                            <small class="text-muted">^GSPC</small>
                                        </div>
                                        <div class="text-end">
                                            <div class="h6 mb-1" id="sp500-price">Loading...</div>
                                            <small id="sp500-change">Loading...</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="stock-card">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1 fw-bold">NASDAQ</h6>
                                            <small class="text-muted">^IXIC</small>
                                        </div>
                                        <div class="text-end">
                                            <div class="h6 mb-1" id="nasdaq-price">Loading...</div>
                                            <small id="nasdaq-change">Loading...</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="stock-card">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1 fw-bold">DOW JONES</h6>
                                            <small class="text-muted">^DJI</small>
                                        </div>
                                        <div class="text-end">
                                            <div class="h6 mb-1" id="dow-price">Loading...</div>
                                            <small id="dow-change">Loading...</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="stock-card">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <h6 class="mb-1 fw-bold">VIX</h6>
                                            <small class="text-muted">Volatility Index</small>
                                        </div>
                                        <div class="text-end">
                                            <div class="h6 mb-1" id="vix-price">Loading...</div>
                                            <small id="vix-change">Loading...</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="py-5" style="background: rgba(255,255,255,0.02);">
            <div class="container">
                <div class="text-center mb-5">
                    <h2 class="section-title">Why Choose PULSE?</h2>
                    <p class="section-subtitle">Professional-grade financial intelligence for sophisticated investors</p>
                </div>
                <div class="row">
                    <div class="col-lg-4 text-center mb-5">
                        <div class="feature-icon">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <h4 class="mb-3">Advanced Analytics</h4>
                        <p class="text-muted">Real-time market data with sophisticated technical indicators and predictive analytics</p>
                    </div>
                    <div class="col-lg-4 text-center mb-5">
                        <div class="feature-icon">
                            <i class="fas fa-search"></i>
                        </div>
                        <h4 class="mb-3">Opportunity Identification</h4>
                        <p class="text-muted">Discover high-potential emerging opportunities with comprehensive fundamental analysis</p>
                    </div>
                    <div class="col-lg-4 text-center mb-5">
                        <div class="feature-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h4 class="mb-3">Risk Management</h4>
                        <p class="text-muted">Comprehensive risk assessment and portfolio protection strategies</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="py-5 border-top border-secondary" style="background: rgba(0,0,0,0.5);">
            <div class="container text-center">
                <p class="text-muted mb-0">&copy; 2024 PULSE Financial Intelligence Platform. Professional-grade market analysis and portfolio management.</p>
            </div>
        </footer>

        <script>
            // Fetch live market data
            function updateMarketData() {
                const symbols = ['^GSPC', '^IXIC', '^DJI', '^VIX'];
                symbols.forEach(symbol => {
                    fetch(`/stock/${symbol}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.price) {
                                const priceElement = document.getElementById(symbol.toLowerCase().replace('^', '') + '-price');
                                const changeElement = document.getElementById(symbol.toLowerCase().replace('^', '') + '-change');
                                
                                if (priceElement && changeElement) {
                                    priceElement.textContent = '$' + data.price;
                                    const changeText = (data.change >= 0 ? '+' : '') + data.change + ' (' + (data.change_percent >= 0 ? '+' : '') + data.change_percent + '%)';
                                    changeElement.textContent = changeText;
                                    changeElement.className = data.change >= 0 ? 'text-success' : 'text-danger';
                                    priceElement.className = 'h6 mb-1 fw-bold ' + (data.change >= 0 ? 'text-success' : 'text-danger');
                                }
                            }
                        })
                        .catch(error => console.error('Error fetching data:', error));
                });
            }

            // Update data every 30 seconds
            updateMarketData();
            setInterval(updateMarketData, 30000);
        </script>
    </body>
    </html>
    ''', featured_stocks=featured_stocks)

@app.route('/stock/<symbol>')
def stock_data(symbol):
    data = get_stock_price(symbol)
    if data['success']:
        return data
    return {'error': 'Unable to fetch data'}, 400

@app.route('/market-pulse')
def market_pulse():
    stats = {
        'sentiment': 'Bullish',
        'fear_greed_index': 65,
        'market_breadth': 'Advancers outnumber decliners',
        'volatility': 'Low',
        'top_sector': 'Technology',
        'bottom_sector': 'Utilities',
        'put_call_ratio': 0.85,
        'advance_decline_ratio': '1.7',
        'market_cap': '45T',
        'volume': 'High',
        'last_updated': 'Just now',
    }
    return render_template_string('''
    <html><head><title>Market Pulse</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body{background:#000;color:#fff;} .stat-card{background:rgba(255,255,255,0.05);border:1px solid #333;padding:2rem;margin-bottom:2rem;border-radius:1rem;}</style></head><body>
    <div class="container-fluid py-5">
        <h1 class="mb-4 text-center">Market Pulse</h1>
        <div class="row justify-content-center">
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Sentiment</h5><div class="display-6">{{ stats['sentiment'] }}</div></div>
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Fear & Greed Index</h5><div class="display-6">{{ stats['fear_greed_index'] }}/100</div></div>
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Market Breadth</h5><div class="display-6">{{ stats['market_breadth'] }}</div></div>
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Volatility</h5><div class="display-6">{{ stats['volatility'] }}</div></div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Top Sector</h5><div class="display-6">{{ stats['top_sector'] }}</div></div>
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Bottom Sector</h5><div class="display-6">{{ stats['bottom_sector'] }}</div></div>
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Put/Call Ratio</h5><div class="display-6">{{ stats['put_call_ratio'] }}</div></div>
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Advance/Decline Ratio</h5><div class="display-6">{{ stats['advance_decline_ratio'] }}</div></div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Market Cap</h5><div class="display-6">{{ stats['market_cap'] }}</div></div>
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Volume</h5><div class="display-6">{{ stats['volume'] }}</div></div>
            <div class="col-md-3 stat-card mx-2 mb-3"><h5>Last Updated</h5><div class="display-6">{{ stats['last_updated'] }}</div></div>
        </div>
        <a href="/" class="btn btn-light mt-4">Back Home</a>
    </div></body></html>
    ''', stats=stats)

@app.route('/underrated-stocks')
def underrated_stocks_page():
    # Get live data for all stocks
    stocks_with_live_data = []
    for stock in emerging_opportunities:
        live_data = get_live_stock_data(stock['symbol'])
        stock_with_data = stock.copy()
        if live_data['success']:
            stock_with_data['current_price'] = f"${live_data['price']}"
            stock_with_data['change'] = live_data['change']
            stock_with_data['change_percent'] = live_data['change_percent']
            stock_with_data['price_color'] = 'text-success' if live_data['change'] >= 0 else 'text-danger'
        else:
            stock_with_data['current_price'] = 'N/A'
            stock_with_data['change'] = 0
            stock_with_data['change_percent'] = 0
            stock_with_data['price_color'] = 'text-muted'
        stocks_with_live_data.append(stock_with_data)
    
    return render_template_string('''
    <html>
    <head>
        <title>Emerging Opportunities - PULSE</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #000 100%);
                color: #fff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .stock-card {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                padding: 2rem;
                margin-bottom: 2rem;
                border-radius: 1rem;
                transition: all 0.3s ease;
            }
            .stock-card:hover {
                background: rgba(255,255,255,0.08);
                border-color: rgba(255,255,255,0.2);
                transform: translateY(-5px);
            }
            .gradient-text {
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            .navbar {
                background: rgba(0,0,0,0.95) !important;
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .logo {
                font-size: 2.2rem;
                font-weight: 800;
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 2px;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
            <div class="container">
                <a class="navbar-brand logo" href="/">
                    <i class="fas fa-chart-line me-2"></i>PULSE
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="{{ url_for('market_pulse') }}">Market Intelligence</a>
                    <a class="nav-link active" href="{{ url_for('underrated_stocks_page') }}">Emerging Opportunities</a>
                    <a class="nav-link" href="{{ url_for('stocks_to_sell_page') }}">Risk Assessment</a>
                    <a class="nav-link" href="{{ url_for('market_news') }}">Market Analysis</a>
                    <a class="nav-link" href="{{ url_for('portfolio_tracker') }}">Portfolio Management</a>
                    <a class="nav-link" href="{{ url_for('performance_comparison') }}">Performance Analytics</a>
                </div>
            </div>
        </nav>

        <div class="container py-5 mt-5">
            <div class="text-center mb-5">
                <h1 class="display-4 gradient-text mb-3">Emerging Investment Opportunities</h1>
                <p class="lead text-muted">High-potential stocks with strong fundamentals and growth prospects</p>
            </div>
            
            <div class="row">
                {% for stock in stocks %}
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="stock-card h-100">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <h4 class="mb-1 fw-bold">{{ stock.symbol }}</h4>
                                <h6 class="text-muted">{{ stock.name }}</h6>
                                <span class="badge bg-secondary">{{ stock.sector }}</span>
                            </div>
                            <div class="text-end">
                                <div class="h5 mb-1 {{ stock.price_color }} fw-bold">{{ stock.current_price }}</div>
                                <small class="{{ stock.price_color }}">
                                    {% if stock.change >= 0 %}+{% endif %}{{ stock.change }} ({% if stock.change_percent >= 0 %}+{% endif %}{{ stock.change_percent }}%)
                                </small>
                            </div>
                        </div>
                        <div class="mb-3">
                            <span class="badge bg-success me-2">{{ stock.recommendation }}</span>
                            <span class="badge bg-warning">Target: {{ stock.target }}</span>
                        </div>
                        <p class="text-muted small mb-2"><strong>Investment Thesis:</strong> {{ stock.reason }}</p>
                        <p class="small">{{ stock.analysis }}</p>
                        <div class="mt-3">
                            <a href="/charts/{{ stock.symbol }}" class="btn btn-sm btn-outline-light">
                                <i class="fas fa-chart-line me-1"></i>Technical Analysis
                            </a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <div class="text-center mt-5">
                <a href="/" class="btn btn-outline-light btn-lg">
                    <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    ''', stocks=stocks_with_live_data)

@app.route('/stocks-to-sell')
def stocks_to_sell_page():
    # Get live data for all stocks to sell
    stocks_with_live_data = []
    for stock in risk_assessment_stocks:
        live_data = get_live_stock_data(stock['symbol'])
        stock_with_data = stock.copy()
        if live_data['success']:
            stock_with_data['current_price'] = f"${live_data['price']}"
            stock_with_data['change'] = live_data['change']
            stock_with_data['change_percent'] = live_data['change_percent']
            stock_with_data['price_color'] = 'text-success' if live_data['change'] >= 0 else 'text-danger'
        else:
            stock_with_data['current_price'] = 'N/A'
            stock_with_data['change'] = 0
            stock_with_data['change_percent'] = 0
            stock_with_data['price_color'] = 'text-muted'
        stocks_with_live_data.append(stock_with_data)
    
    return render_template_string('''
    <html>
    <head>
        <title>Risk Assessment - PULSE</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #000 100%);
                color: #fff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .stock-card {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                padding: 2rem;
                margin-bottom: 2rem;
                border-radius: 1rem;
                transition: all 0.3s ease;
            }
            .stock-card:hover {
                background: rgba(255,255,255,0.08);
                border-color: rgba(255,255,255,0.2);
                transform: translateY(-5px);
            }
            .gradient-text {
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            .navbar {
                background: rgba(0,0,0,0.95) !important;
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .logo {
                font-size: 2.2rem;
                font-weight: 800;
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 2px;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
            <div class="container">
                <a class="navbar-brand logo" href="/">
                    <i class="fas fa-chart-line me-2"></i>PULSE
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="{{ url_for('market_pulse') }}">Market Intelligence</a>
                    <a class="nav-link" href="{{ url_for('underrated_stocks_page') }}">Emerging Opportunities</a>
                    <a class="nav-link active" href="{{ url_for('stocks_to_sell_page') }}">Risk Assessment</a>
                    <a class="nav-link" href="{{ url_for('market_news') }}">Market Analysis</a>
                    <a class="nav-link" href="{{ url_for('portfolio_tracker') }}">Portfolio Management</a>
                    <a class="nav-link" href="{{ url_for('performance_comparison') }}">Performance Analytics</a>
                </div>
            </div>
        </nav>

        <div class="container py-5 mt-5">
            <div class="text-center mb-5">
                <h1 class="display-4 gradient-text mb-3">Risk Assessment Analysis</h1>
                <p class="lead text-muted">Comprehensive evaluation of stocks requiring careful consideration and risk management</p>
            </div>
            
            <div class="row">
                {% for stock in stocks %}
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="stock-card h-100">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <h4 class="mb-1 fw-bold">{{ stock.symbol }}</h4>
                                <h6 class="text-muted">{{ stock.name }}</h6>
                                <span class="badge bg-secondary">{{ stock.sector }}</span>
                            </div>
                            <div class="text-end">
                                <div class="h5 mb-1 {{ stock.price_color }} fw-bold">{{ stock.current_price }}</div>
                                <small class="{{ stock.price_color }}">
                                    {% if stock.change >= 0 %}+{% endif %}{{ stock.change }} ({% if stock.change_percent >= 0 %}+{% endif %}{{ stock.change_percent }}%)
                                </small>
                            </div>
                        </div>
                        <div class="mb-3">
                            <span class="badge bg-danger me-2">{{ stock.recommendation }}</span>
                            <span class="badge bg-warning">Target: {{ stock.target }}</span>
                        </div>
                        <p class="text-muted small mb-2"><strong>Risk Factors:</strong> {{ stock.reason }}</p>
                        <p class="small">{{ stock.analysis }}</p>
                        <div class="mt-3">
                            <a href="/charts/{{ stock.symbol }}" class="btn btn-sm btn-outline-light">
                                <i class="fas fa-chart-line me-1"></i>Technical Analysis
                            </a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <div class="text-center mt-5">
                <a href="/" class="btn btn-outline-light btn-lg">
                    <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    ''', stocks=stocks_with_live_data)

@app.route('/market-news')
def market_news():
    return render_template_string('''
    <html>
    <head>
        <title>Market Analysis - PULSE</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #000 100%);
                color: #fff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .news-card {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                padding: 2rem;
                margin-bottom: 2rem;
                border-radius: 1rem;
                transition: all 0.3s ease;
            }
            .news-card:hover {
                background: rgba(255,255,255,0.08);
                border-color: rgba(255,255,255,0.2);
                transform: translateY(-5px);
            }
            .gradient-text {
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            .navbar {
                background: rgba(0,0,0,0.95) !important;
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .logo {
                font-size: 2.2rem;
                font-weight: 800;
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 2px;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
            <div class="container">
                <a class="navbar-brand logo" href="/">
                    <i class="fas fa-chart-line me-2"></i>PULSE
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="{{ url_for('market_pulse') }}">Market Intelligence</a>
                    <a class="nav-link" href="{{ url_for('underrated_stocks_page') }}">Emerging Opportunities</a>
                    <a class="nav-link" href="{{ url_for('stocks_to_sell_page') }}">Risk Assessment</a>
                    <a class="nav-link active" href="{{ url_for('market_news') }}">Market Analysis</a>
                    <a class="nav-link" href="{{ url_for('portfolio_tracker') }}">Portfolio Management</a>
                    <a class="nav-link" href="{{ url_for('performance_comparison') }}">Performance Analytics</a>
                </div>
            </div>
        </nav>

        <div class="container-fluid py-5 mt-5">
            <div class="text-center mb-5">
                <h1 class="display-4 gradient-text mb-3">Market Analysis & Insights</h1>
                <p class="lead text-muted">Comprehensive market intelligence and strategic analysis</p>
            </div>
            
            <div class="row justify-content-center">
                {% for news in news_list %}
                <div class="col-md-5 news-card mx-3 mb-4">
                    <h4 class="fw-bold mb-3">{{ news.title }}</h4>
                    <p class="mb-3">{{ news.summary }}</p>
                    <div class="mb-3">
                        <strong>Strategic Analysis:</strong><br>
                        <small>{{ news.details }}</small>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="badge bg-info">{{ news.impact }}</span>
                        <small class="text-muted">{{ news.time }}</small>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <div class="text-center mt-5">
                <a href="/" class="btn btn-outline-light btn-lg">
                    <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>
    </body>
    </html>
    ''', news_list=financial_news)

@app.route('/charts/<symbol>')
def stock_charts(symbol):
    period = request.args.get('period', '6mo')
    chart_data = get_stock_chart_data(symbol, period)
    
    if not chart_data:
        return render_template_string('''
        <html><head><title>Chart Error</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"></head>
        <body style="background:#000;color:#fff;">
        <div class="container py-5 text-center">
            <h1>Chart Not Available</h1>
            <p>Unable to load chart data for {{ symbol }}</p>
            <a href="/" class="btn btn-light">Back Home</a>
        </div></body></html>
        ''', symbol=symbol)
    
    return render_template_string('''
    <html><head><title>{{ symbol }} Charts</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns"></script>
    <style>body{background:#000;color:#fff;} .chart-container{background:rgba(255,255,255,0.05);border:1px solid #333;border-radius:10px;padding:20px;margin:20px 0;}</style>
    </head><body>
    <div class="container py-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>{{ symbol }} - Interactive Charts</h1>
            <div>
                <a href="?period=1mo" class="btn btn-outline-light btn-sm">1M</a>
                <a href="?period=3mo" class="btn btn-outline-light btn-sm">3M</a>
                <a href="?period=6mo" class="btn btn-outline-light btn-sm">6M</a>
                <a href="?period=1y" class="btn btn-outline-light btn-sm">1Y</a>
                <a href="/" class="btn btn-light btn-sm">Home</a>
            </div>
        </div>
        
        <!-- Candlestick Chart -->
        <div class="chart-container">
            <h3>Candlestick Chart with Moving Averages</h3>
            <canvas id="candlestickChart" width="800" height="400"></canvas>
        </div>
        
        <!-- RSI Chart -->
        <div class="chart-container">
            <h3>RSI (Relative Strength Index)</h3>
            <canvas id="rsiChart" width="800" height="200"></canvas>
        </div>
        
        <!-- MACD Chart -->
        <div class="chart-container">
            <h3>MACD (Moving Average Convergence Divergence)</h3>
            <canvas id="macdChart" width="800" height="200"></canvas>
        </div>
        
        <!-- Volume Chart -->
        <div class="chart-container">
            <h3>Volume</h3>
            <canvas id="volumeChart" width="800" height="150"></canvas>
        </div>
    </div>
    
    <script>
        const chartData = {{ chart_data | tojson }};
        
        // Candlestick Chart
        const candlestickCtx = document.getElementById('candlestickChart').getContext('2d');
        new Chart(candlestickCtx, {
            type: 'line',
            data: {
                labels: chartData.map(d => d.date),
                datasets: [{
                    label: 'Close Price',
                    data: chartData.map(d => d.close),
                    borderColor: '#fff',
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    fill: false
                }, {
                    label: 'MA20',
                    data: chartData.map(d => d.ma20),
                    borderColor: '#ff6b6b',
                    backgroundColor: 'rgba(255,107,107,0.1)',
                    fill: false
                }, {
                    label: 'MA50',
                    data: chartData.map(d => d.ma50),
                    borderColor: '#4ecdc4',
                    backgroundColor: 'rgba(78,205,196,0.1)',
                    fill: false
                }, {
                    label: 'MA200',
                    data: chartData.map(d => d.ma200),
                    borderColor: '#45b7d1',
                    backgroundColor: 'rgba(69,183,209,0.1)',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    x: { ticks: { color: '#fff' } },
                    y: { ticks: { color: '#fff' } }
                }
            }
        });
        
        // RSI Chart
        const rsiCtx = document.getElementById('rsiChart').getContext('2d');
        new Chart(rsiCtx, {
            type: 'line',
            data: {
                labels: chartData.map(d => d.date),
                datasets: [{
                    label: 'RSI',
                    data: chartData.map(d => d.rsi),
                    borderColor: '#ffd93d',
                    backgroundColor: 'rgba(255,217,61,0.1)',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    x: { ticks: { color: '#fff' } },
                    y: { 
                        ticks: { color: '#fff' },
                        min: 0,
                        max: 100
                    }
                }
            }
        });
        
        // MACD Chart
        const macdCtx = document.getElementById('macdChart').getContext('2d');
        new Chart(macdCtx, {
            type: 'line',
            data: {
                labels: chartData.map(d => d.date),
                datasets: [{
                    label: 'MACD',
                    data: chartData.map(d => d.macd),
                    borderColor: '#6c5ce7',
                    backgroundColor: 'rgba(108,92,231,0.1)',
                    fill: false
                }, {
                    label: 'Signal',
                    data: chartData.map(d => d.signal),
                    borderColor: '#fd79a8',
                    backgroundColor: 'rgba(253,121,168,0.1)',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    x: { ticks: { color: '#fff' } },
                    y: { ticks: { color: '#fff' } }
                }
            }
        });
        
        // Volume Chart
        const volumeCtx = document.getElementById('volumeChart').getContext('2d');
        new Chart(volumeCtx, {
            type: 'bar',
            data: {
                labels: chartData.map(d => d.date),
                datasets: [{
                    label: 'Volume',
                    data: chartData.map(d => d.volume),
                    backgroundColor: 'rgba(255,255,255,0.3)',
                    borderColor: '#fff',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#fff' }
                    }
                },
                scales: {
                    x: { ticks: { color: '#fff' } },
                    y: { ticks: { color: '#fff' } }
                }
            }
        });
    </script>
    </body></html>
    ''', symbol=symbol, chart_data=chart_data)

@app.route('/portfolio')
def portfolio_tracker():
    return render_template_string('''
    <html><head><title>Portfolio Tracker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body{background:#000;color:#fff;} .portfolio-card{background:rgba(255,255,255,0.05);border:1px solid #333;border-radius:10px;padding:20px;margin:20px 0;}</style>
    </head><body>
    <div class="container py-5">
        <h1 class="mb-4">Portfolio Tracker</h1>
        
        <!-- Sample Portfolios -->
        <div class="row">
            <div class="col-md-4">
                <div class="portfolio-card">
                    <h4>Tech Portfolio</h4>
                    <p class="text-muted">AAPL, MSFT, GOOGL, AMZN, NVDA</p>
                    <button class="btn btn-primary" onclick="loadPortfolio('tech_portfolio')">View Performance</button>
                </div>
            </div>
            <div class="col-md-4">
                <div class="portfolio-card">
                    <h4>Growth Portfolio</h4>
                    <p class="text-muted">TSLA, NFLX, META, CRM, ADBE</p>
                    <button class="btn btn-primary" onclick="loadPortfolio('growth_portfolio')">View Performance</button>
                </div>
            </div>
            <div class="col-md-4">
                <div class="portfolio-card">
                    <h4>Value Portfolio</h4>
                    <p class="text-muted">JNJ, PG, KO, WMT, JPM</p>
                    <button class="btn btn-primary" onclick="loadPortfolio('value_portfolio')">View Performance</button>
                </div>
            </div>
        </div>
        
        <!-- Custom Portfolio -->
        <div class="portfolio-card mt-4">
            <h4>Create Custom Portfolio</h4>
            <div class="row">
                <div class="col-md-8">
                    <input type="text" id="customSymbols" class="form-control" placeholder="Enter symbols separated by commas (e.g., AAPL,MSFT,GOOGL)">
                </div>
                <div class="col-md-4">
                    <button class="btn btn-success" onclick="loadCustomPortfolio()">Track Portfolio</button>
                </div>
            </div>
        </div>
        
        <!-- Portfolio Performance Results -->
        <div id="portfolioResults" class="portfolio-card mt-4" style="display:none;">
            <h4 id="portfolioTitle">Portfolio Performance</h4>
            <div id="portfolioTable"></div>
        </div>
        
        <a href="/" class="btn btn-light mt-4">Back Home</a>
    </div>
    
    <script>
        async function loadPortfolio(portfolioType) {
            const portfolios = {
                'tech_portfolio': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA'],
                'growth_portfolio': ['TSLA', 'NFLX', 'META', 'CRM', 'ADBE'],
                'value_portfolio': ['JNJ', 'PG', 'KO', 'WMT', 'JPM']
            };
            
            const symbols = portfolios[portfolioType];
            await fetchPortfolioData(symbols, portfolioType.replace('_', ' ').toUpperCase());
        }
        
        async function loadCustomPortfolio() {
            const symbolsInput = document.getElementById('customSymbols').value;
            const symbols = symbolsInput.split(',').map(s => s.trim().toUpperCase()).filter(s => s);
            
            if (symbols.length === 0) {
                alert('Please enter valid stock symbols');
                return;
            }
            
            await fetchPortfolioData(symbols, 'Custom Portfolio');
        }
        
        async function fetchPortfolioData(symbols, title) {
            try {
                const response = await fetch('/api/portfolio-performance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ symbols: symbols })
                });
                
                const data = await response.json();
                displayPortfolioResults(data, title);
            } catch (error) {
                console.error('Error fetching portfolio data:', error);
            }
        }
        
        function displayPortfolioResults(data, title) {
            const resultsDiv = document.getElementById('portfolioResults');
            const titleDiv = document.getElementById('portfolioTitle');
            const tableDiv = document.getElementById('portfolioTable');
            
            titleDiv.textContent = title;
            
            let tableHTML = `
                <table class="table table-dark">
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Start Price</th>
                            <th>End Price</th>
                            <th>Change</th>
                            <th>Change %</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            data.forEach(stock => {
                if (stock.success) {
                    const changeClass = stock.change_percent >= 0 ? 'text-success' : 'text-danger';
                    const changeIcon = stock.change_percent >= 0 ? '▲' : '▼';
                    
                    tableHTML += `
                        <tr>
                            <td><strong>${stock.symbol}</strong></td>
                            <td>$${stock.start_price}</td>
                            <td>$${stock.end_price}</td>
                            <td class="${changeClass}">${changeIcon} $${Math.abs(stock.change)}</td>
                            <td class="${changeClass}">${changeIcon} ${Math.abs(stock.change_percent)}%</td>
                        </tr>
                    `;
                } else {
                    tableHTML += `
                        <tr>
                            <td><strong>${stock.symbol}</strong></td>
                            <td colspan="4" class="text-muted">Data unavailable</td>
                        </tr>
                    `;
                }
            });
            
            tableHTML += '</tbody></table>';
            tableDiv.innerHTML = tableHTML;
            resultsDiv.style.display = 'block';
        }
    </script>
    </body></html>
    ''')

@app.route('/api/portfolio-performance', methods=['POST'])
def api_portfolio_performance():
    data = request.get_json()
    symbols = data.get('symbols', [])
    performance_data = get_portfolio_performance(symbols)
    return jsonify(performance_data)

@app.route('/performance-comparison')
def performance_comparison():
    # Compare emerging opportunities vs established stocks
    emerging_symbols = [stock['symbol'] for stock in emerging_opportunities[:5]]
    established_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']
    
    emerging_performance = get_portfolio_performance(emerging_symbols)
    established_performance = get_portfolio_performance(established_symbols)
    
    return render_template_string('''
    <html>
    <head>
        <title>Performance Analytics - PULSE</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #000 100%);
                color: #fff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .comparison-card {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 25px;
                margin: 20px 0;
                transition: all 0.3s ease;
            }
            .comparison-card:hover {
                background: rgba(255,255,255,0.08);
                border-color: rgba(255,255,255,0.2);
                transform: translateY(-3px);
            }
            .gradient-text {
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            .navbar {
                background: rgba(0,0,0,0.95) !important;
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .logo {
                font-size: 2.2rem;
                font-weight: 800;
                background: linear-gradient(45deg, #fff, #ccc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 2px;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
            <div class="container">
                <a class="navbar-brand logo" href="/">
                    <i class="fas fa-chart-line me-2"></i>PULSE
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="{{ url_for('market_pulse') }}">Market Intelligence</a>
                    <a class="nav-link" href="{{ url_for('underrated_stocks_page') }}">Emerging Opportunities</a>
                    <a class="nav-link" href="{{ url_for('stocks_to_sell_page') }}">Risk Assessment</a>
                    <a class="nav-link" href="{{ url_for('market_news') }}">Market Analysis</a>
                    <a class="nav-link" href="{{ url_for('portfolio_tracker') }}">Portfolio Management</a>
                    <a class="nav-link active" href="{{ url_for('performance_comparison') }}">Performance Analytics</a>
                </div>
            </div>
        </nav>

        <div class="container py-5 mt-5">
            <div class="text-center mb-5">
                <h1 class="display-4 gradient-text mb-3">Performance Analytics</h1>
                <p class="lead text-muted">Comparative analysis of emerging opportunities versus established market leaders</p>
            </div>
            
            <div class="row">
                <div class="col-lg-6">
                    <div class="comparison-card">
                        <h3 class="gradient-text mb-4">Performance Comparison Analysis</h3>
                        <canvas id="comparisonChart" width="400" height="300"></canvas>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="comparison-card">
                        <h3 class="gradient-text mb-4">Analytical Summary</h3>
                        <div id="summaryTable"></div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-lg-6">
                    <div class="comparison-card">
                        <h4 class="gradient-text mb-3">Emerging Opportunities Performance</h4>
                        <div id="emergingTable"></div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="comparison-card">
                        <h4 class="gradient-text mb-3">Established Leaders Performance</h4>
                        <div id="establishedTable"></div>
                    </div>
                </div>
            </div>
            
            <div class="text-center mt-5">
                <a href="/" class="btn btn-outline-light btn-lg">
                    <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
                </a>
            </div>
        </div>
        
        <script>
            const emergingData = {{ emerging_performance | tojson }};
            const establishedData = {{ established_performance | tojson }};
            
            // Calculate averages
            const emergingAvg = emergingData.filter(d => d.success).reduce((sum, d) => sum + d.change_percent, 0) / emergingData.filter(d => d.success).length;
            const establishedAvg = establishedData.filter(d => d.success).reduce((sum, d) => sum + d.change_percent, 0) / establishedData.filter(d => d.success).length;
            
            // Comparison Chart
            const ctx = document.getElementById('comparisonChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Emerging Opportunities', 'Established Leaders'],
                    datasets: [{
                        label: 'Average Performance (%)',
                        data: [emergingAvg, establishedAvg],
                        backgroundColor: ['rgba(255,255,255,0.8)', 'rgba(255,193,7,0.8)'],
                        borderColor: ['#fff', '#ffc107'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: '#fff' }
                        }
                    },
                    scales: {
                        y: { 
                            ticks: { color: '#fff' },
                            grid: { color: 'rgba(255,255,255,0.1)' }
                        },
                        x: { 
                            ticks: { color: '#fff' },
                            grid: { color: 'rgba(255,255,255,0.1)' }
                        }
                    }
                }
            });
            
            // Summary Table
            document.getElementById('summaryTable').innerHTML = `
                <table class="table table-dark">
                    <tr><td><strong>Emerging Opportunities Avg:</strong></td><td class="${emergingAvg >= 0 ? 'text-success' : 'text-danger'} fw-bold">${emergingAvg.toFixed(2)}%</td></tr>
                    <tr><td><strong>Established Leaders Avg:</strong></td><td class="${establishedAvg >= 0 ? 'text-success' : 'text-danger'} fw-bold">${establishedAvg.toFixed(2)}%</td></tr>
                    <tr><td><strong>Performance Differential:</strong></td><td class="${(emergingAvg - establishedAvg) >= 0 ? 'text-success' : 'text-danger'} fw-bold">${(emergingAvg - establishedAvg).toFixed(2)}%</td></tr>
                </table>
            `;
            
            // Performance Tables
            function createTable(data, tableId) {
                let html = '<table class="table table-dark table-sm"><thead><tr><th>Symbol</th><th>Performance %</th></tr></thead><tbody>';
                data.forEach(stock => {
                    if (stock.success) {
                        const changeClass = stock.change_percent >= 0 ? 'text-success' : 'text-danger';
                        const changeIcon = stock.change_percent >= 0 ? '▲' : '▼';
                        html += `<tr><td><strong>${stock.symbol}</strong></td><td class="${changeClass} fw-bold">${changeIcon} ${Math.abs(stock.change_percent).toFixed(2)}%</td></tr>`;
                    }
                });
                html += '</tbody></table>';
                document.getElementById(tableId).innerHTML = html;
            }
            
            createTable(emergingData, 'emergingTable');
            createTable(establishedData, 'establishedTable');
        </script>
    </body>
    </html>
    ''', emerging_performance=emerging_performance, established_performance=established_performance)

if __name__ == '__main__':
    app.run(debug=True, port=8080) 