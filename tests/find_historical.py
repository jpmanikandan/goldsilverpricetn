from bs4 import BeautifulSoup

filename = "page_cloudscraper.html"

try:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find element containing "Last 10 Days"
    elements = soup.find_all(string=lambda text: "Last 10 Days" in text if text else False)
    print(f"Found {len(elements)} elements with 'Last 10 Days'.")
    
    for i, element in enumerate(elements):
        parent = element.parent
        print(f"\nElement {i} parent: <{parent.name} class='{parent.get('class')}'>")
        print(f"Content: {parent.get_text(strip=True)[:100]}...")
        
        # Find next table
        sibling = parent.find_next_sibling()
        if sibling:
            print(f"Next sibling: <{sibling.name} class='{sibling.get('class')}'>")
            if sibling.name == 'table':
                print("Found table next to header!")
                rows = sibling.find_all("tr")
                print(f"Table has {len(rows)} rows")
                for row in rows[:5]:
                    cols = row.find_all(["th", "td"])
                    print(" | ".join([col.get_text(strip=True) for col in cols]))

except Exception as e:
    print(f"Error: {e}")
