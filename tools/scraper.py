import cloudscraper
from bs4 import BeautifulSoup
from langchain.tools import tool

@tool
def get_current_prices_trichy(city: str = "Trichy") -> str:
    """
    Fetches the current gold (24K, 22K, 18K) and silver prices from GoodReturns.in.
    Args:
        city: The city name (default: "Trichy"). Extract from queries like "[City: Chennai]".
    Returns:
        str: A string containing all current metal prices for the specified city.
    """
    # Normalize city name for URL (lowercase, handle spaces)
    city_url = city.lower().replace(" ", "-")
    url = f"https://www.goodreturns.in/gold-rates/{city_url}.html"
    
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        result = f"Current Prices in {city}:\n\n"
        
        # Find 24 Carat Gold
        header_24k = soup.find(lambda tag: tag.name == "h2" and "24 Carat" in tag.get_text())
        if header_24k:
            table_24k = header_24k.find_next_sibling("table")
            if table_24k:
                result += "24 Carat Gold:\n"
                rows = table_24k.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        gram = cols[0].get_text(strip=True)
                        price = cols[1].get_text(strip=True)
                        result += f"- {gram}: {price}\n"
                result += "\n"
        
        # Find 22 Carat Gold
        header_22k = soup.find(lambda tag: tag.name == "h2" and "22 Carat" in tag.get_text())
        if header_22k:
            table_22k = header_22k.find_next_sibling("table")
            if table_22k:
                result += "22 Carat Gold:\n"
                rows = table_22k.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        gram = cols[0].get_text(strip=True)
                        price = cols[1].get_text(strip=True)
                        result += f"- {gram}: {price}\n"
                result += "\n"
        
        # Find 18 Carat Gold
        header_18k = soup.find(lambda tag: tag.name == "h2" and "18 Carat" in tag.get_text())
        if header_18k:
            table_18k = header_18k.find_next_sibling("table")
            if table_18k:
                result += "18 Carat Gold:\n"
                rows = table_18k.find_all("tr")
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        gram = cols[0].get_text(strip=True)
                        price = cols[1].get_text(strip=True)
                        result += f"- {gram}: {price}\n"
                result += "\n"
        
        # Fetch Silver prices from silver-rates page
        try:
            silver_url = f"https://www.goodreturns.in/silver-rates/{city_url}.html"
            silver_response = scraper.get(silver_url)
            silver_response.raise_for_status()
            
            silver_soup = BeautifulSoup(silver_response.text, 'html.parser')
            
            # Find Silver Rate header
            header_silver = silver_soup.find(lambda tag: tag.name == "h2" and "Silver Price Per Gram" in tag.get_text())
            if header_silver:
                table_silver = header_silver.find_next_sibling("table")
                if table_silver:
                    result += "Silver:\n"
                    rows = table_silver.find_all("tr")
                    for row in rows[1:]:
                        cols = row.find_all("td")
                        if len(cols) >= 2:
                            gram = cols[0].get_text(strip=True)
                            price = cols[1].get_text(strip=True)
                            result += f"- {gram}: {price}\n"
        except Exception as silver_error:
            result += f"Silver: (Could not fetch - {str(silver_error)})\n"
        
        return result if result != f"Current Prices in {city}:\n\n" else f"Error: Could not extract price data for {city}."

    except Exception as e:
        return f"Error fetching prices for {city}: {str(e)}"


@tool
def get_historical_prices(metal: str = "24K") -> str:
    """
    Fetches the last 10 days of gold/silver prices in Trichy.
    Args:
        metal: The metal type - "24K", "22K", "18K", or "Silver" (default: "24K")
    Returns:
        str: A string containing the historical prices with dates.
    """
    metal = metal.upper()
    
    # Handle silver separately as it's on a different page
    if metal == "SILVER":
        try:
            silver_url = "https://www.goodreturns.in/silver-rates/trichy.html"
            scraper = cloudscraper.create_scraper()
            response = scraper.get(silver_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            header = soup.find(lambda tag: tag.name == "h2" and "Last 10 Days" in tag.get_text())
            
            if not header:
                return "Error: Could not find 'Last 10 Days' section for silver."
                
            table = header.find_next_sibling("table")
            if not table:
                return "Error: Could not find historical silver price table."
                
            # Silver table has: Date | 10 gram | 100 gram | 1 Kg
            # We'll use the 10 gram column (index 1) and convert to per gram
            rows = table.find_all("tr")
            result = "Silver Rate in Trichy - Last 10 Days (per gram):\n"
            
            for row in rows[1:]:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    date = cols[0].get_text(strip=True)
                    price_10g = cols[1].get_text(strip=True)
                    # Extract price and calculate per gram
                    price_clean = price_10g.split('(')[0]
                    price_clean = price_clean.replace('₹', '').replace(',', '').strip()
                    if price_clean:
                        try:
                            price_per_10g = float(price_clean)
                            price_per_gram = price_per_10g / 10
                            result += f"- {date}: ₹{price_per_gram:.2f}/gram\n"
                        except ValueError:
                            continue
            return result
        except Exception as e:
            return f"Error fetching silver historical prices: {str(e)}"
    
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
            return "Error: Could not find 'Last 10 Days' section on the page."
            
        # Find the table next to it
        table = header.find_next_sibling("table")
        if not table:
            return "Error: Could not find historical price table."
            
        # Determine which column to use
        # Note: The table might have columns: Date, 24K, 22K (and possibly 18K)
        # We need to check the header row first
        header_row = table.find("tr")
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(["th", "td"])]
            try:
                col_index = headers.index(metal) if metal in headers else None
            except ValueError:
                col_index = None
        else:
            # Fallback to old logic
            col_index = 1 if metal == "24K" else 2 if metal == "22K" else 3 if metal == "18K" else None
        
        if col_index is None:
            return f"Error: '{metal}' column not found in historical data. Available: {', '.join(headers[1:]) if header_row else 'Unknown'}"
        
        # Extract rows
        rows = table.find_all("tr")
        
        result = f"{metal} Gold Rate in Trichy - Last 10 Days (1 gram):\n"
        
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) > col_index:
                date = cols[0].get_text(strip=True)
                price = cols[col_index].get_text(strip=True)
                result += f"- {date}: {price}\n"
                
        return result

    except Exception as e:
        return f"Error fetching historical prices: {str(e)}"
