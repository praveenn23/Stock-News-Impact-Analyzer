import requests
import feedparser
from datetime import datetime

def fetch_headlines():
    """Fetches financial news headlines from Yahoo Finance and CNBC RSS feeds."""
    headlines = []
    
    # Yahoo Finance and CNBC RSS feeds
    rss_feeds = [
        "https://finance.yahoo.com/news/rssindex",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    ]
    
    for feed_url in rss_feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:  # Get first 5 headlines from each feed
                title = entry.get('title', '').strip()
                if title and len(title) > 10:
                    headlines.append(title)
        except Exception as e:
            print(f"Error fetching from {feed_url}: {e}")
            continue
    
    if not headlines:
        print("No headlines found from Yahoo Finance or CNBC. Using sample data.")
        headlines = [
            "Stocks rally as Fed signals rate pause",
            "Tech companies report strong earnings",
            "Market volatility increases amid economic uncertainty",
            "Oil prices surge on supply concerns",
            "Cryptocurrency market shows mixed signals"
        ]
    
    return headlines

if __name__ == "__main__":
    headlines = fetch_headlines()
    for h in headlines:
        print(h) 