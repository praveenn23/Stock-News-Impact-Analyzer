from scraper import fetch_headlines
from preprocess import clean_text
from simple_preprocess import simple_clean_text
from sentiment_model import predict_sentiment
from stock_analyzer import analyze_headline_impact
import pandas as pd

def main():
    print("Fetching headlines...")
    headlines = fetch_headlines()
    
    if not headlines:
        print("No headlines fetched. Using sample data for demonstration.")
        headlines = [
            "Apple stock surges on strong iPhone sales",
            "Tech sector faces volatility amid AI concerns", 
            "Oil prices decline affecting energy stocks",
            "Market rally continues as Fed signals rate cuts",
            "Tesla reports record quarterly earnings"
        ]
    
    print(f"Fetched {len(headlines)} headlines.")
    
    # Clean and predict sentiment with fallback
    cleaned = []
    for h in headlines:
        try:
            cleaned_text = clean_text(h)
        except:
            # Fallback to simple preprocessing if NLTK fails
            cleaned_text = simple_clean_text(h)
        cleaned.append(cleaned_text)
    
    sentiments = predict_sentiment(cleaned)
    
    print("\n" + "="*100)
    print("📈 STOCK-SPECIFIC NEWS IMPACT ANALYSIS 📉")
    print("="*100)
    
    # Analyze each headline for specific stock/sector impact
    all_analyses = []
    for i, (headline, sentiment) in enumerate(zip(headlines, sentiments), 1):
        analysis = analyze_headline_impact(headline, sentiment)
        all_analyses.append(analysis)
        
        print(f"\n{i}. 📰 HEADLINE: {headline}")
        print(f"   🎯 SENTIMENT: {sentiment}")
        print(f"   📊 IMPACT ANALYSIS:")
        
        if analysis['analysis']:
            for impact in analysis['analysis']:
                print(f"      {impact}")
        else:
            print(f"      🌐 General Market: {sentiment}")
        
        print("-" * 80)
    
    # Summary statistics by stock/sector
    print(f"\n" + "="*60)
    print("📊 SUMMARY BY STOCK/SECTOR")
    print("="*60)
    
    # Collect all affected stocks and sectors
    stock_impacts = {}
    sector_impacts = {}
    
    for analysis in all_analyses:
        sentiment = analysis['sentiment']
        
        # Count stock impacts
        for stock in analysis['affected_stocks']:
            ticker = stock['ticker']
            if ticker not in stock_impacts:
                stock_impacts[ticker] = {'rise': 0, 'fall': 0, 'stable': 0}
            
            if 'rise' in sentiment.lower():
                stock_impacts[ticker]['rise'] += 1
            elif 'fall' in sentiment.lower():
                stock_impacts[ticker]['fall'] += 1
            else:
                stock_impacts[ticker]['stable'] += 1
        
        # Count sector impacts
        for sector in analysis['affected_sectors']:
            if sector not in sector_impacts:
                sector_impacts[sector] = {'rise': 0, 'fall': 0, 'stable': 0}
            
            if 'rise' in sentiment.lower():
                sector_impacts[sector]['rise'] += 1
            elif 'fall' in sentiment.lower():
                sector_impacts[sector]['fall'] += 1
            else:
                sector_impacts[sector]['stable'] += 1
    
    # Display stock-specific summary
    if stock_impacts:
        print("\n📈 STOCK-SPECIFIC PREDICTIONS:")
        for ticker, impacts in stock_impacts.items():
            total = sum(impacts.values())
            if total > 0:
                dominant = max(impacts, key=impacts.get)
                print(f"   📊 {ticker}: {dominant.upper()} ({impacts[dominant]}/{total} headlines)")
    
    # Display sector-specific summary
    if sector_impacts:
        print("\n🏭 SECTOR-SPECIFIC PREDICTIONS:")
        for sector, impacts in sector_impacts.items():
            total = sum(impacts.values())
            if total > 0:
                dominant = max(impacts, key=impacts.get)
                print(f"   🏭 {sector}: {dominant.upper()} ({impacts[dominant]}/{total} headlines)")
    
    # Overall market sentiment
    print(f"\n" + "="*50)
    print("🎯 OVERALL MARKET SENTIMENT")
    print("="*50)
    
    def map_sentiment_to_trend(sentiment):
        s = sentiment.lower()
        if 'positive' in s or 'rise' in s:
            return 'rise'
        elif 'negative' in s or 'fall' in s:
            return 'fall'
        elif 'neutral' in s or 'stable' in s:
            return 'stable'
        else:
            return 'unknown'

    mapped_trends = [map_sentiment_to_trend(s) for s in sentiments]
    rise_count = mapped_trends.count('rise')
    fall_count = mapped_trends.count('fall')
    stable_count = mapped_trends.count('stable')
    
    print(f"📈 Rise predictions: {rise_count}")
    print(f"📉 Fall predictions: {fall_count}")
    print(f"➡️  Stable predictions: {stable_count}")
    
    if rise_count > fall_count and rise_count > stable_count:
        print("   🟢 BULLISH - More positive news suggests market may rise")
    elif fall_count > rise_count and fall_count > stable_count:
        print("   🔴 BEARISH - More negative news suggests market may fall")
    else:
        print("   🟡 NEUTRAL - Mixed signals suggest market may remain stable")

if __name__ == "__main__":
    main() 