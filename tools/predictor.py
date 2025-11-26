import cloudscraper
from bs4 import BeautifulSoup
from langchain.tools import tool
from tools.silver_helper import predict_silver_price

@tool
def predict_tomorrow_price(metal: str = "24K") -> str:
    """
    Predicts tomorrow's gold/silver price in Trichy based on the last 10 days of historical data.
    Args:
        metal: The metal type - "24K", "22K", "18K", or "Silver" (default: "24K")
    Returns:
        str: A prediction with explanation of the methodology.
    """
    metal = metal.upper()
    
    # Handle silver separately
    if metal == "SILVER":
        return predict_silver_price()
    
    # Handle gold prices
    url = "https://www.goodreturns.in/gold-rates/trichy.html"
    
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the header for "Last 10 Days"
        header = soup.find(lambda tag: tag.name == "h2" and "Last 10 Days" in tag.get_text())
        
        if not header:
            return "Error: Could not find historical data for prediction."
            
        # Find the table next to it
        table = header.find_next_sibling("table")
        if not table:
            return "Error: Could not find historical price table."
        
        # Determine which column to use
        # Check header row first
        header_row = table.find("tr")
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
            try:
                col_index = headers.index(metal) if metal in headers else None
            except ValueError:
                col_index = None
        else:
            # Fallback
            col_index = 1 if metal == "24K" else 2 if metal == "22K" else 3 if metal == "18K" else None
        
        if col_index is None:
            return f"Error: '{metal}' column not found. Available: {', '.join(headers[1:]) if header_row else 'Unknown'}"
            
        # Extract rows
        rows = table.find_all("tr")
        
        prices = []
        dates = []
        
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) > col_index:
                date_str = cols[0].get_text(strip=True)
                price_text = cols[col_index].get_text(strip=True)
                # Extract numeric value from price (format: ₹12,688(+186) or ₹12,688)
                # First, remove everything after '(' if present
                price_clean = price_text.split('(')[0]
                # Then remove Rupee symbol, commas, and spaces
                price_clean = price_clean.replace('₹', '').replace(',', '').strip()
                if price_clean:
                    try:
                        prices.append(float(price_clean))
                        dates.append(date_str)
                    except ValueError:
                        continue
                
        if len(prices) < 3:
            return "Error: Not enough historical data for prediction (need at least 3 days)."
        
        # Calculate metrics
        avg_price = sum(prices) / len(prices)
        recent_avg = sum(prices[:3]) / 3  # Last 3 days average
        
        # Calculate trend (simple linear regression slope)
        n = len(prices)
        x_vals = list(range(n))
        x_mean = sum(x_vals) / n
        y_mean = avg_price
        
        numerator = sum((x_vals[i] - x_mean) * (prices[i] - y_mean) for i in range(n))
        denominator = sum((x_vals[i] - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        
        # Predict tomorrow's price
        predicted_price = prices[0] + slope
        
        # Determine trend
        if slope > 5:
            trend = "increasing"
        elif slope < -5:
            trend = "decreasing"
        else:
            trend = "stable"
        
        # Calculate volatility
        variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
        std_dev = variance ** 0.5
        
        result = f"""{metal} Gold Price Prediction for Tomorrow (1 gram):
        
Predicted Price: Rs. {predicted_price:.2f}
Confidence Range: Rs. {predicted_price - std_dev:.2f} - Rs. {predicted_price + std_dev:.2f}

Analysis:
- Current Price (Today): Rs. {prices[0]:.2f}
- 10-Day Average: Rs. {avg_price:.2f}
- Recent 3-Day Average: Rs. {recent_avg:.2f}
- Trend: {trend.capitalize()} (slope: {slope:.2f})
- Volatility (Std Dev): Rs. {std_dev:.2f}

Note: This prediction is based on simple statistical analysis of the last {len(prices)} days.
Gold prices are influenced by many factors including global markets, currency exchange rates,
and economic conditions. This should be used as a rough estimate only.
"""
        
        return result

    except Exception as e:
        return f"Error predicting price: {str(e)}"
