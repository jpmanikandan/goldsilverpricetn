import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from tools.scraper import get_current_prices_trichy, get_historical_prices
    from tools.predictor import predict_tomorrow_price
    
    print("=== Testing Current Prices ===")
    result = get_current_prices_trichy.invoke({})
    print(result)
    
    print("\n=== Testing Historical Prices (24K) ===")
    result = get_historical_prices.invoke({"metal": "24K"})
    print(result[:300] + "...")
    
    print("\n=== Testing Historical Prices (22K) ===")
    result = get_historical_prices.invoke({"metal": "22K"})
    print(result[:300] + "...")
    
    print("\n=== Testing Prediction (24K) ===")
    result = predict_tomorrow_price.invoke({"metal": "24K"})
    print(result)
    
    print("\n=== Testing Prediction (22K) ===")
    result = predict_tomorrow_price.invoke({"metal": "22K"})
    print(result)
    
    print("\nAll tests completed successfully!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
