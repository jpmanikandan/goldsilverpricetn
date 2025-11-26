from bs4 import BeautifulSoup

filename = "page_cloudscraper.html"

try:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the header for "Last 10 Days"
    header = soup.find(lambda tag: tag.name == "h2" and "Last 10 Days" in tag.get_text())
    
    output = []
    
    if header:
        table = header.find_next_sibling("table")
        if table:
            rows = table.find_all("tr")
            output.append(f"Found {len(rows)} rows\n")
            
            for i, row in enumerate(rows[:5]):
                cols = row.find_all(["th", "td"])
                output.append(f"\nRow {i}:\n")
                for j, col in enumerate(cols):
                    text = col.get_text(strip=True)
                    output.append(f"  Col {j}: '{text}'\n")
                    output.append(f"  Col {j} repr: {repr(text)}\n")
    
    # Write to file
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        f.writelines(output)
    
    print("Debug output written to debug_output.txt")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
