# 💰 Gold and Silver Price Prediction by BellLabs

An AI-powered application for real-time gold and silver price tracking, historical analysis, and price predictions for Tamil Nadu cities.

![BellLabs](assets/belllabs_logo.jpg)

## 🌟 Features

- **Multi-City Support**: Track prices across 10 Tamil Nadu cities (Chennai, Trichy, Madurai, Salem, Coimbatore, Vellore, Tirunelveli, Erode, Namakkal, Thanjavur)
- **Multiple Gold Types**: 24K, 22K, and 18K gold prices
- **Silver Rates**: Real-time silver price tracking
- **AI Predictions**: Tomorrow's price forecasts using statistical analysis
- **Historical Data**: Last 10 days price trends
- **Interactive UI**: Premium dark-themed interface with golden accents
- **Quick Actions**: One-click feature buttons for instant queries

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API Key

### Installation

1. **Clone or download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## 📖 Usage

### City Selection
- Use the dropdown in the sidebar to select your city
- Chat history clears when you change cities

### Quick Actions (Sidebar Buttons)
- **🏆 24K Gold Prices** - Get current 24K gold price
- **🥈 Silver Rates** - Get current silver price
- **📊 AI Predictions** - Predict tomorrow's 24K gold price
- **📈 Historical Data** - View last 10 days of prices

### Chat Interface
Ask questions like:
- "What are the current gold and silver prices?"
- "Show me the last 10 days of 22K gold prices"
- "Predict tomorrow's 18K gold price"
- "Compare 24K and 22K gold prices"

## 📁 Project Structure

```
goldrate/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── verify_setup.py        # Setup verification script
├── assets/                # Images and static files
│   └── belllabs_logo.jpg
├── agent/                 # LangChain agent
│   └── core.py           # Agent configuration
├── tools/                 # AI agent tools
│   ├── scraper.py        # Web scraping for prices
│   ├── predictor.py      # Price prediction logic
│   └── silver_helper.py  # Silver-specific helpers
├── tests/                 # Test scripts and outputs
└── docs/                  # Documentation
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **AI/ML**: LangChain 0.3.27 + OpenAI GPT-3.5
- **Web Scraping**: Cloudscraper + BeautifulSoup4
- **Data Source**: GoodReturns.in
- **Prediction**: Statistical analysis (Linear Regression, Moving Averages)

## 🎨 Design Features

- **Premium Dark Theme**: Navy blue gradient background
- **Golden Accents**: Matching the gold price theme
- **Animated Logo**: Glowing pulse effect
- **Glassmorphism**: Translucent chat messages
- **Responsive Layout**: Wide layout for better space utilization
- **Custom Font**: Poppins for modern aesthetics

## 📊 Prediction Methodology

The AI uses statistical analysis including:
- **Simple Moving Average**: 10-day average price
- **Linear Regression**: Trend analysis and slope calculation
- **Volatility Analysis**: Standard deviation for confidence ranges

## 🔒 Privacy & Security

- API keys stored in environment variables
- No data collection or storage
- Real-time data fetching from public sources

## 🤝 Support

For issues or questions, contact BellLabs.

## 📄 License

Proprietary - BellLabs © 2025

---

**Powered by BellLabs** | *Innovation in AI*
