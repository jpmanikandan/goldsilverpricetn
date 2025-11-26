def predict_silver_price() -> str:
    """Helper function to predict silver price."""
    import cloudscraper
    from bs4 import BeautifulSoup
    
    url = "https://www.goodreturns.in/silver-rates/trichy.html"
    
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        header = soup.find(lambda tag: tag.name == "h2" and "Last 10 Days" in tag.get_text())
        
        if not header:
            return "Error: Could not find historical data for silver prediction."
            
        table = header.find_next_sibling("table")
        if not table:
            return "Error: Could not find historical silver price table."
        
        # Extract rows - silver table has: Date | 10 gram | 100 gram | 1 Kg
        rows = table.find_all("tr")
        
        prices = []
        dates = []
        
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) >= 2:
                date_str = cols[0].get_text(strip=True)
                price_10g = cols[1].get_text(strip=True)
                # Extract price and calculate per gram
                price_clean = price_10g.split('(')[0]
                price_clean = price_clean.replace('₹', '').replace(',', '').strip()
                if price_clean:
                    try:
                        price_per_10g = float(price_clean)
                        price_per_gram = price_per_10g / 10
                        prices.append(price_per_gram)
                        dates.append(date_str)
                    except ValueError:
                        continue
                
        if len(prices) < 3:
            return "Error: Not enough historical data for silver prediction (need at least 3 days)."
        
        # Calculate metrics
        avg_price = sum(prices) / len(prices)
        recent_avg = sum(prices[:3]) / 3
        
        # Calculate trend
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
        if slope > 0.5:
            trend = "increasing"
        elif slope < -0.5:
            trend = "decreasing"
        else:
            trend = "stable"
        
        # Calculate volatility
        variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
        std_dev = variance ** 0.5
        
        result = f"""Silver Price Prediction for Tomorrow (per gram):
        
Predicted Price: Rs. {predicted_price:.2f}
Confidence Range: Rs. {predicted_price - std_dev:.2f} - Rs. {predicted_price + std_dev:.2f}

Analysis:
- Current Price (Today): Rs. {prices[0]:.2f}
- 10-Day Average: Rs. {avg_price:.2f}
- Recent 3-Day Average: Rs. {recent_avg:.2f}
- Trend: {trend.capitalize()} (slope: {slope:.2f})
- Volatility (Std Dev): Rs. {std_dev:.2f}

Note: This prediction is based on simple statistical analysis of the last {len(prices)} days.
Silver prices are influenced by many factors including global markets, currency exchange rates,
and economic conditions. This should be used as a rough estimate only.
"""
        
        return result

    except Exception as e:
        return f"Error predicting silver price: {str(e)}"
