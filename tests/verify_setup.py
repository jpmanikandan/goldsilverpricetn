import os
import sys
from dotenv import load_dotenv

def check_imports():
    print("Checking imports...")
    try:
        import streamlit
        print("✅ streamlit imported")
        import langchain
        print(f"✅ langchain imported (version: {langchain.__version__})")
        from langchain_openai import ChatOpenAI
        print("✅ langchain_openai imported")
        from alpha_vantage.foreignexchange import ForeignExchange
        print("✅ alpha_vantage imported")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    return True

def check_keys():
    print("\nChecking API Keys...")
    load_dotenv()
    openai_key = os.environ.get("OPENAI_API_KEY")
    av_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    
    if openai_key:
        print("✅ OPENAI_API_KEY found")
    else:
        print("⚠️ OPENAI_API_KEY not found in environment")
        
    if av_key:
        print("✅ ALPHAVANTAGE_API_KEY found")
    else:
        print("⚠️ ALPHAVANTAGE_API_KEY not found in environment")
        
    return bool(openai_key and av_key)

def test_tool():
    print("\nTesting Gold Price Tool...")
    load_dotenv()
    if not os.environ.get("ALPHAVANTAGE_API_KEY"):
        print("⚠️ Skipping tool test: ALPHAVANTAGE_API_KEY not set")
        return

    try:
        # Add current directory to path to import tools
        sys.path.append(os.getcwd())
        from tools.gold_price import get_gold_price_india
        
        # Invoke the tool directly
        result = get_gold_price_india.invoke({})
        print(f"Tool Output: {result}")
        
        if "Error" not in result:
            print("✅ Tool test passed")
        else:
            print("⚠️ Tool test returned an error (check API key quota or validity)")
            
    except Exception as e:
        print(f"❌ Tool test failed: {e}")

if __name__ == "__main__":
    if check_imports():
        check_keys()
        test_tool()
    print("\nVerification complete.")
