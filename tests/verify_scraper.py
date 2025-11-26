import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from tools.scraper import get_gold_price_trichy
    print("Scraper tool imported successfully.")
    
    print("Running scraper tool...")
    result = get_gold_price_trichy.invoke({})
    print(f"Result:\n{result}")
    
    if "Error" not in result and "24 Carat" in result:
        print("Scraper tool verification passed!")
    else:
        print("Scraper tool verification failed (unexpected output).")

except Exception as e:
    print(f"Error verifying scraper: {e}")
