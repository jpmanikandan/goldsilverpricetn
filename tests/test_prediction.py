import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from tools.predictor import predict_tomorrow_gold_price
    print("Prediction tool imported successfully.")
    
    print("\nRunning prediction tool...")
    result = predict_tomorrow_gold_price.invoke({})
    print(f"Result:\n{result}")
    
    if "Error" not in result and "Predicted Price" in result:
        print("\nPrediction tool verification passed!")
    else:
        print("\nPrediction tool verification failed (unexpected output).")

except Exception as e:
    print(f"Error verifying prediction: {e}")
    import traceback
    traceback.print_exc()
