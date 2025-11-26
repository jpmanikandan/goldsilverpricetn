import cloudscraper
from bs4 import BeautifulSoup

url = "https://www.goodreturns.in/gold-rates/trichy.html"

try:
    print("Creating scraper...")
    scraper = cloudscraper.create_scraper()
    print(f"Fetching {url}...")
    response = scraper.get(url)
    response.raise_for_status()
    
    print("Page fetched successfully.")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to find the 24k gold price
    # Based on common structures, let's look for tables or specific text
    # I'll print the title and some text to verify content
    print(f"Title: {soup.title.string}")
    
    # Save to file for inspection if needed
    with open("page_cloudscraper.html", "w", encoding="utf-8") as f:
        f.write(response.text)
        
    # Heuristic search for 24k price
    # Usually in a table with class 'gold_silver_table' or similar
    tables = soup.find_all("table")
    print(f"Found {len(tables)} tables.")
    
except Exception as e:
    print(f"Error fetching page with cloudscraper: {e}")
