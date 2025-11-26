import requests

url = "https://www.goodreturns.in/gold-rates/trichy.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("✅ Page fetched successfully.")
except Exception as e:
    print(f"❌ Error fetching page: {e}")
