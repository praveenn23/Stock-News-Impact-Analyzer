# Stock News Impact Analyzer - Flask Web App

A modern web application that analyzes financial news headlines and predicts their impact on stock prices using AI-powered sentiment analysis. This Flask-based web app provides both a user-friendly web interface and REST API endpoints.

## 🌟 Features

### Web Interface
- **Interactive Dashboard**: Beautiful, responsive web interface for easy analysis
- **Real-time Analysis**: Get instant sentiment analysis of financial news
- **Stock-Specific Filtering**: Analyze news impact on specific stocks or sectors
- **Visual Charts**: Interactive charts showing sentiment distribution
- **Detailed Results**: Comprehensive breakdown of news impact analysis

### API Endpoints
- **REST API**: Programmatic access to analysis functionality
- **JSON Responses**: Structured data for integration with other applications
- **Multiple Endpoints**: Different endpoints for various use cases

### Core Functionality
- **News Scraping**: Fetches latest financial headlines from major sources
- **AI Sentiment Analysis**: Uses machine learning to predict market sentiment
- **Stock Impact Analysis**: Identifies specific stocks and sectors affected by news
- **Market Trend Prediction**: Overall market sentiment analysis

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd Stock-News-Impact-Analyze

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Web Application

```bash
# Start the Flask server
python app.py
```

The application will be available at: **http://localhost:5000**

### 3. Usage

#### Web Interface
1. Open your browser and go to `http://localhost:5000`
2. Optionally enter a stock ticker (e.g., AAPL, TSLA, GOOGL)
3. Click "Analyze News Impact" to get results
4. View detailed analysis with charts and statistics

#### API Usage

**Analyze specific stock:**
```bash
curl "http://localhost:5000/api/analyze?ticker=AAPL"
```

**Get list of stocks in recent news:**
```bash
curl "http://localhost:5000/api/stocks"
```

**General market analysis:**
```bash
curl "http://localhost:5000/api/analyze"
```

## 📊 API Documentation

### Endpoints

#### `GET /api/analyze`
Analyzes news headlines and returns sentiment analysis.

**Parameters:**
- `ticker` (optional): Stock ticker symbol (e.g., AAPL, TSLA)

**Response:**
```json
{
  "status": "success",
  "timestamp": "2024-01-15T10:30:00",
  "stock_ticker": "AAPL",
  "headlines_analyzed": 5,
  "analyses": [
    {
      "headline": "Apple stock surges on strong iPhone sales",
      "sentiment": "positive",
      "analysis": ["Apple Inc. likely to see stock price increase"],
      "affected_stocks": [{"ticker": "AAPL", "name": "Apple Inc."}],
      "affected_sectors": ["Technology"]
    }
  ]
}
```

#### `GET /api/stocks`
Returns list of stocks mentioned in recent news.

**Response:**
```json
{
  "status": "success",
  "stocks": ["AAPL", "TSLA", "GOOGL"],
  "count": 3
}
```

## 🏗️ Project Structure

```
Stock News Impact Analyze/
├── app.py                 # Main Flask application
├── main.py               # Original command-line version
├── scraper.py            # News scraping functionality
├── preprocess.py         # Text preprocessing
├── sentiment_model.py    # ML sentiment analysis
├── stock_analyzer.py     # Stock impact analysis
├── templates/            # HTML templates
│   ├── index.html       # Homepage
│   ├── results.html     # Results page
│   └── error.html       # Error page
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_DEBUG`: Set to `1` to enable debug features

### Customization
- Modify `scraper.py` to add new news sources
- Update `sentiment_model.py` to use different ML models
- Customize templates in `templates/` directory

## 🛠️ Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

### Running in Production
```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 📈 Features in Detail

### Sentiment Analysis
- **Positive**: News likely to cause stock price increases
- **Negative**: News likely to cause stock price decreases  
- **Neutral**: News unlikely to significantly impact prices

### Stock Impact Detection
- Automatically identifies mentioned stocks in headlines
- Maps company names to stock tickers
- Analyzes sector-wide impacts

### Market Trend Analysis
- Aggregates sentiment across all headlines
- Provides overall market sentiment (Bullish/Bearish/Neutral)
- Shows sentiment distribution with interactive charts

## 🔒 Security Considerations

- Input validation for stock tickers
- Error handling for failed requests
- Rate limiting (can be added for production)
- CORS configuration for API access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the error logs in the Flask application
2. Verify all dependencies are installed
3. Ensure news sources are accessible
4. Check network connectivity

## 🔄 Migration from Command Line

If you're migrating from the command-line version:

1. **Keep existing files**: All original functionality is preserved
2. **New web interface**: `app.py` provides the web interface
3. **API access**: New REST endpoints for programmatic access
4. **Same analysis**: Uses the same underlying analysis logic

The original `main.py` still works for command-line usage! 