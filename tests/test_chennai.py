import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from tools.scraper import get_current_prices_trichy
    
    print("Testing Chennai prices...")
    result = get_current_prices_trichy.invoke({"city": "Chennai"})
    
    # Write to file
    with open("chennai_prices.txt", "w", encoding="utf-8") as f:
        f.write(result)
    
    print("Output written to chennai_prices.txt")
    print("\nTest completed!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
