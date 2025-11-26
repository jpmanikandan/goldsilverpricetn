import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from tools.predictor import predict_tomorrow_price
    
    print("Testing silver prediction...")
    result = predict_tomorrow_price.invoke({"metal": "Silver"})
    
    # Write to file
    with open("silver_prediction_output.txt", "w", encoding="utf-8") as f:
        f.write(result)
    
    print("Output written to silver_prediction_output.txt")
    print("\nTest completed!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
