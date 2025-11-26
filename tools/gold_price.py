import os
import streamlit as st
from langchain.tools import tool
from alpha_vantage.foreignexchange import ForeignExchange

@tool
def get_gold_price_india() -> str:
    """
    Fetches the current gold price in India (approximated by XAU to INR exchange rate)
    using the Alpha Vantage API.
    Returns:
        str: A string containing the current exchange rate of Gold (XAU) to Indian Rupee (INR).
    """
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    if not api_key:
        return "Error: ALPHAVANTAGE_API_KEY not found in environment variables."

    try:
        cc = ForeignExchange(key=api_key)
        # There is no direct "Gold Price" endpoint for India in free tier usually,
        # but XAU (Gold Ounce) to INR is the standard way to track it.
        data, _ = cc.get_currency_exchange_rate(from_currency='XAU', to_currency='INR')
        
        # Debug: Show raw data in sidebar
        with st.sidebar:
            st.subheader("Debug Info")
            st.json(data)
        
        # data is a dict like:
        # {
        #     '1. From_Currency Code': 'XAU',
        #     '2. From_Currency Name': 'Gold (troy ounce)',
        #     '3. To_Currency Code': 'INR',
        #     '4. To_Currency Name': 'Indian Rupee',
        #     '5. Exchange Rate': '200000.00',
        #     ...
        # }
        
        rate = data.get('5. Exchange Rate')
        if rate:
            return f"The current price of Gold (XAU) in India is {rate} INR per troy ounce."
        else:
            return "Error: Could not retrieve exchange rate from Alpha Vantage response."

    except Exception as e:
        return f"Error fetching gold price: {str(e)}"
