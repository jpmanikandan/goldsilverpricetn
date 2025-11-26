import os
from dotenv import load_dotenv
from alpha_vantage.foreignexchange import ForeignExchange
import json

def debug_alpha_vantage():
    load_dotenv()
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    
    if not api_key:
        print("❌ ALPHAVANTAGE_API_KEY not found in environment.")
        return

    print(f"🔑 Using API Key: {api_key[:4]}...{api_key[-4:] if len(api_key) > 4 else ''}")
    
    try:
        cc = ForeignExchange(key=api_key)
        print("📡 Fetching XAU to INR...")
        data, meta_data = cc.get_currency_exchange_rate(from_currency='XAU', to_currency='INR')
        
        print("\n📊 Raw Data:")
        print(json.dumps(data, indent=2))
        
        rate = data.get('5. Exchange Rate')
        if rate:
            print(f"\n✅ Exchange Rate found: {rate}")
        else:
            print("\n⚠️ Exchange Rate NOT found in data.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        # Alpha Vantage library often raises ValueError for API errors
        if "Thank you for using Alpha Vantage" in str(e) or "call frequency" in str(e):
            print("💡 Hint: This usually means API rate limit exceeded or invalid key.")

if __name__ == "__main__":
    debug_alpha_vantage()
