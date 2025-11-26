import cloudscraper
from bs4 import BeautifulSoup

url = "https://www.goodreturns.in/gold-rates/trichy.html"

try:
    scraper = cloudscraper.create_scraper()
    print(f"Fetching {url}...")
    response = scraper.get(url)
    response.raise_for_status()
    
    print("Page fetched successfully.")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all h2 tags
    h2_tags = soup.find_all("h2")
    print(f"\nFound {len(h2_tags)} h2 tags:")
    
    output = []
    for i, h2 in enumerate(h2_tags):
        text = h2.get_text(strip=True)
        output.append(f"\nH2 {i}: {text}\n")
        
        if "18" in text or "Carat" in text:
            output.append(f"*** MATCH: Contains '18' or 'Carat' ***\n")
            output.append(f"Class: {h2.get('class')}\n")
            
            # Check next sibling
            sibling = h2.find_next_sibling()
            if sibling:
                output.append(f"Next sibling: <{sibling.name}>\n")
                if sibling.name == "table":
                    rows = sibling.find_all("tr")
                    output.append(f"Table has {len(rows)} rows\n")
                    for row in rows[:3]:
                        cols = row.find_all(["th", "td"])
                        output.append(" | ".join([col.get_text(strip=True) for col in cols]) + "\n")
    
    # Write to file
    with open("gold_18k_check.txt", "w", encoding="utf-8") as f:
        f.writelines(output)
    
    print("Structure written to gold_18k_check.txt")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
