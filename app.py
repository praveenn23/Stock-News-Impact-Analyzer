from flask import Flask, render_template, request, jsonify
from scraper import fetch_headlines
from preprocess import clean_text
from simple_preprocess import simple_clean_text
from sentiment_model import predict_sentiment
from stock_analyzer import analyze_headline_impact
import pandas as pd
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Main page with form for stock analysis"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze news headlines and return results"""
    try:
        # Get user input
        stock_ticker = request.form.get('stock_ticker', '').upper().strip()
        
        # Fetch headlines
        print("Fetching headlines...")
        headlines = fetch_headlines()
        
        if not headlines:
            # Fallback to sample data
            headlines = [
                "Apple stock surges on strong iPhone sales",
                "Tech sector faces volatility amid AI concerns", 
                "Oil prices decline affecting energy stocks",
                "Market rally continues as Fed signals rate cuts",
                "Tesla reports record quarterly earnings"
            ]
        
        # Process headlines
        cleaned = []
        for h in headlines:
            try:
                cleaned_text = clean_text(h)
            except:
                cleaned_text = simple_clean_text(h)
            cleaned.append(cleaned_text)
        
        sentiments = predict_sentiment(cleaned)
        
        # Analyze each headline
        all_analyses = []
        for headline, sentiment in zip(headlines, sentiments):
            analysis = analyze_headline_impact(headline, sentiment)
            all_analyses.append(analysis)
        
        # Filter by stock ticker if specified
        if stock_ticker:
            filtered_analyses = []
            for analysis in all_analyses:
                affected_stocks = [stock.get('ticker', '') for stock in analysis.get('affected_stocks', [])]
                if stock_ticker in affected_stocks:
                    filtered_analyses.append(analysis)
            all_analyses = filtered_analyses
        
        # Prepare summary statistics
        stock_impacts = {}
        sector_impacts = {}
        
        for analysis in all_analyses:
            sentiment = analysis.get('sentiment', '')
            
            # Count stock impacts
            for stock in analysis.get('affected_stocks', []):
                ticker = stock.get('ticker', '')
                if ticker and ticker != 'MARKET':  # Skip general market indicators
                    if ticker not in stock_impacts:
                        stock_impacts[ticker] = {'rise': 0, 'fall': 0, 'stable': 0}
                    
                    if 'rise' in sentiment.lower() or 'positive' in sentiment.lower():
                        stock_impacts[ticker]['rise'] += 1
                    elif 'fall' in sentiment.lower() or 'negative' in sentiment.lower():
                        stock_impacts[ticker]['fall'] += 1
                    else:
                        stock_impacts[ticker]['stable'] += 1
            
            # Count sector impacts
            for sector in analysis.get('affected_sectors', []):
                if sector not in sector_impacts:
                    sector_impacts[sector] = {'rise': 0, 'fall': 0, 'stable': 0}
                
                if 'rise' in sentiment.lower() or 'positive' in sentiment.lower():
                    sector_impacts[sector]['rise'] += 1
                elif 'fall' in sentiment.lower() or 'negative' in sentiment.lower():
                    sector_impacts[sector]['fall'] += 1
                else:
                    sector_impacts[sector]['stable'] += 1
        
        # Overall market sentiment
        mapped_trends = []
        for sentiment in sentiments:
            s = sentiment.lower()
            if 'positive' in s or 'rise' in s:
                mapped_trends.append('rise')
            elif 'negative' in s or 'fall' in s:
                mapped_trends.append('fall')
            elif 'neutral' in s or 'stable' in s:
                mapped_trends.append('stable')
            else:
                mapped_trends.append('unknown')

        rise_count = mapped_trends.count('rise')
        fall_count = mapped_trends.count('fall')
        stable_count = mapped_trends.count('stable')
        
        # Determine overall market sentiment
        if rise_count > fall_count and rise_count > stable_count:
            overall_sentiment = "BULLISH - More positive news suggests market may rise"
        elif fall_count > rise_count and fall_count > stable_count:
            overall_sentiment = "BEARISH - More negative news suggests market may fall"
        else:
            overall_sentiment = "NEUTRAL - Mixed signals suggest market may remain stable"
        
        return render_template('results.html',
                             analyses=all_analyses,
                             stock_impacts=stock_impacts,
                             sector_impacts=sector_impacts,
                             overall_sentiment=overall_sentiment,
                             rise_count=rise_count,
                             fall_count=fall_count,
                             stable_count=stable_count,
                             stock_ticker=stock_ticker,
                             analysis_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    except Exception as e:
        print(f"Error in analyze route: {str(e)}")
        return render_template('error.html', error=str(e))

@app.route('/api/analyze', methods=['GET'])
def api_analyze():
    """API endpoint for programmatic access"""
    try:
        stock_ticker = request.args.get('ticker', '').upper().strip()
        
        # Fetch and analyze headlines (same logic as above)
        headlines = fetch_headlines()
        
        if not headlines:
            headlines = [
                "Apple stock surges on strong iPhone sales",
                "Tech sector faces volatility amid AI concerns", 
                "Oil prices decline affecting energy stocks",
                "Market rally continues as Fed signals rate cuts",
                "Tesla reports record quarterly earnings"
            ]
        
        # Process headlines
        cleaned = []
        for h in headlines:
            try:
                cleaned_text = clean_text(h)
            except:
                cleaned_text = simple_clean_text(h)
            cleaned.append(cleaned_text)
        
        sentiments = predict_sentiment(cleaned)
        
        # Analyze headlines
        all_analyses = []
        for headline, sentiment in zip(headlines, sentiments):
            analysis = analyze_headline_impact(headline, sentiment)
            all_analyses.append(analysis)
        
        # Filter by ticker if specified
        if stock_ticker:
            filtered_analyses = []
            for analysis in all_analyses:
                affected_stocks = [stock.get('ticker', '') for stock in analysis.get('affected_stocks', [])]
                if stock_ticker in affected_stocks:
                    filtered_analyses.append(analysis)
            all_analyses = filtered_analyses
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'stock_ticker': stock_ticker,
            'headlines_analyzed': len(all_analyses),
            'analyses': all_analyses
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/stocks')
def api_stocks():
    """API endpoint to get list of stocks mentioned in recent news"""
    try:
        headlines = fetch_headlines()
        
        if not headlines:
            headlines = [
                "Apple stock surges on strong iPhone sales",
                "Tech sector faces volatility amid AI concerns", 
                "Oil prices decline affecting energy stocks",
                "Market rally continues as Fed signals rate cuts",
                "Tesla reports record quarterly earnings"
            ]
        
        # Process headlines
        cleaned = []
        for h in headlines:
            try:
                cleaned_text = clean_text(h)
            except:
                cleaned_text = simple_clean_text(h)
            cleaned.append(cleaned_text)
        
        sentiments = predict_sentiment(cleaned)
        
        # Get all mentioned stocks
        all_stocks = set()
        for headline, sentiment in zip(headlines, sentiments):
            analysis = analyze_headline_impact(headline, sentiment)
            for stock in analysis.get('affected_stocks', []):
                ticker = stock.get('ticker', '')
                if ticker and ticker != 'MARKET':  # Skip general market indicators
                    all_stocks.add(ticker)
        
        return jsonify({
            'status': 'success',
            'stocks': list(all_stocks),
            'count': len(all_stocks)
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# © [current year] Praveen Kumar. All rights reserved. 