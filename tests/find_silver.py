from bs4 import BeautifulSoup

filename = "page_cloudscraper.html"

try:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    output = []
    
    # Find all h2 tags
    h2_tags = soup.find_all("h2")
    output.append(f"Found {len(h2_tags)} h2 tags\n\n")
    
    for i, h2 in enumerate(h2_tags):
        text = h2.get_text(strip=True)
        if "silver" in text.lower() or "Silver" in text:
            output.append(f"H2 {i}: {text}\n")
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
            output.append("\n")
    
    # Write to file
    with open("silver_debug.txt", "w", encoding="utf-8") as f:
        f.writelines(output)
    
    print("Debug output written to silver_debug.txt")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
