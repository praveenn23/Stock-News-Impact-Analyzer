import re
import pandas as pd

# Common stock tickers and company names
STOCK_DATABASE = {
    # Tech stocks
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'TSLA': 'Tesla Inc.',
    'META': 'Meta Platforms Inc.',
    'NVDA': 'NVIDIA Corporation',
    'NFLX': 'Netflix Inc.',
    'AMD': 'Advanced Micro Devices',
    'INTC': 'Intel Corporation',
    
    # Financial stocks
    'JPM': 'JPMorgan Chase & Co.',
    'BAC': 'Bank of America Corp.',
    'WFC': 'Wells Fargo & Company',
    'GS': 'Goldman Sachs Group Inc.',
    'MS': 'Morgan Stanley',
    
    # Energy stocks
    'XOM': 'Exxon Mobil Corporation',
    'CVX': 'Chevron Corporation',
    'COP': 'ConocoPhillips',
    'EOG': 'EOG Resources Inc.',
    
    # Healthcare stocks
    'JNJ': 'Johnson & Johnson',
    'PFE': 'Pfizer Inc.',
    'UNH': 'UnitedHealth Group Inc.',
    'ABBV': 'AbbVie Inc.',
    
    # Consumer stocks
    'KO': 'Coca-Cola Company',
    'PEP': 'PepsiCo Inc.',
    'WMT': 'Walmart Inc.',
    'HD': 'Home Depot Inc.',
    'MCD': 'McDonald\'s Corporation',
    
    # ETFs and Indices
    'SPY': 'SPDR S&P 500 ETF',
    'QQQ': 'Invesco QQQ Trust',
    'DIA': 'SPDR Dow Jones Industrial Average ETF',
    'VTI': 'Vanguard Total Stock Market ETF',
    '^GSPC': 'S&P 500 Index',
    '^DJI': 'Dow Jones Industrial Average',
    '^IXIC': 'NASDAQ Composite'
}

# Sector keywords
SECTOR_KEYWORDS = {
    'Technology': ['tech', 'technology', 'software', 'hardware', 'semiconductor', 'ai', 'artificial intelligence', 'cloud', 'digital'],
    'Financial': ['bank', 'financial', 'finance', 'investment', 'lending', 'credit', 'mortgage', 'insurance'],
    'Energy': ['oil', 'gas', 'energy', 'petroleum', 'renewable', 'solar', 'wind', 'fossil fuel'],
    'Healthcare': ['healthcare', 'medical', 'pharmaceutical', 'biotech', 'drug', 'hospital', 'insurance'],
    'Consumer': ['retail', 'consumer', 'e-commerce', 'shopping', 'food', 'beverage', 'automotive'],
    'Real Estate': ['real estate', 'property', 'housing', 'construction', 'mortgage'],
    'Industrial': ['industrial', 'manufacturing', 'aerospace', 'defense', 'machinery'],
    'Materials': ['materials', 'mining', 'chemical', 'steel', 'aluminum', 'copper']
}

def extract_stocks_and_sectors(headline):
    """Extract stock tickers, company names, and sectors from a headline."""
    headline_upper = headline.upper()
    headline_lower = headline.lower()
    
    found_stocks = []
    found_sectors = []
    
    # Extract stock tickers
    for ticker, company in STOCK_DATABASE.items():
        if ticker in headline_upper or company.upper() in headline_upper:
            found_stocks.append({
                'ticker': ticker,
                'company': company,
                'type': 'specific_stock'
            })
    
    # Extract sectors
    for sector, keywords in SECTOR_KEYWORDS.items():
        for keyword in keywords:
            if keyword in headline_lower:
                found_sectors.append(sector)
                break
    
    # If no specific stocks found, try to identify general market indicators
    if not found_stocks:
        market_indicators = {
            'market': 'Overall Market',
            'stocks': 'Overall Market',
            'equity': 'Overall Market',
            'wall street': 'Overall Market',
            'trading': 'Overall Market'
        }
        
        for indicator, description in market_indicators.items():
            if indicator in headline_lower:
                found_stocks.append({
                    'ticker': 'MARKET',
                    'company': description,
                    'type': 'market_indicator'
                })
                break
    
    return found_stocks, list(set(found_sectors))

def analyze_headline_impact(headline, sentiment):
    """Analyze the specific impact of a headline on stocks/sectors."""
    stocks, sectors = extract_stocks_and_sectors(headline)
    
    analysis = {
        'headline': headline,
        'sentiment': sentiment,
        'affected_stocks': stocks,
        'affected_sectors': sectors,
        'analysis': []
    }
    
    # Generate specific analysis for each stock/sector
    for stock in stocks:
        if stock['type'] == 'specific_stock':
            analysis['analysis'].append(
                f"📊 {stock['ticker']} ({stock['company']}): {sentiment}"
            )
        else:
            analysis['analysis'].append(
                f"📈 {stock['company']}: {sentiment}"
            )
    
    for sector in sectors:
        analysis['analysis'].append(
            f"🏭 {sector} Sector: {sentiment}"
        )
    
    # If no specific stocks/sectors found, provide general analysis
    if not stocks and not sectors:
        analysis['analysis'].append(
            f"🌐 General Market: {sentiment}"
        )
    
    return analysis

if __name__ == "__main__":
    test_headlines = [
        "Apple stock surges on strong iPhone sales",
        "Tech sector faces volatility amid AI concerns",
        "Oil prices decline affecting energy stocks",
        "Market rally continues as Fed signals rate cuts"
    ]
    
    for headline in test_headlines:
        result = analyze_headline_impact(headline, "rise (high confidence)")
        print(f"\nHeadline: {result['headline']}")
        print("Impact Analysis:")
        for analysis in result['analysis']:
            print(f"  {analysis}")
        print("-" * 50) 