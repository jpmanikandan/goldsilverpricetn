# Language translations for the app

TRANSLATIONS = {
    "en": {
        "title": "💰 Gold and Silver Price Prediction",
        "subtitle": "Powered by BellLabs AI | Real-time predictions for Tamil Nadu cities",
        "config": "⚙️ Configuration",
        "select_city": "📍 Select City",
        "select_language": "🌐 Language",
        "features": "✨ Features",
        "gold_24k": "🏆 24K Gold Prices",
        "silver": "🥈 Silver Rates",
        "predictions": "📊 AI Predictions",
        "historical": "📈 Historical Data",
        "brand_footer": "🏢 BellLabs<br>Innovation in AI",
        "chat_placeholder": "Ask about gold/silver prices, predictions, or trends...",
        "error": "⚠️ An error occurred",
        "query_24k": "What is the current 24K gold price in {city}?",
        "query_silver": "What is the current silver price in {city}?",
        "query_predict": "Predict tomorrow's 24K gold price in {city}",
        "query_historical": "Show me the last 10 days of 24K gold prices in {city}"
    },
    "ta": {
        "title": "💰 தங்கம் மற்றும் வெள்ளி விலை கணிப்பு",
        "subtitle": "பெல்லேப்ஸ் AI மூலம் இயக்கப்படுகிறது | தமிழ்நாடு நகரங்களுக்கான நேரடி கணிப்புகள்",
        "config": "⚙️ அமைப்புகள்",
        "select_city": "📍 நகரத்தைத் தேர்ந்தெடுக்கவும்",
        "select_language": "🌐 மொழி",
        "features": "✨ அம்சங்கள்",
        "gold_24k": "🏆 24K தங்க விலைகள்",
        "silver": "🥈 வெள்ளி விலைகள்",
        "predictions": "📊 AI கணிப்புகள்",
        "historical": "📈 வரலாற்று தரவு",
        "brand_footer": "🏢 பெல்லேப்ஸ்<br>AI இல் புதுமை",
        "chat_placeholder": "தங்கம்/வெள்ளி விலைகள், கணிப்புகள் அல்லது போக்குகளைப் பற்றி கேளுங்கள்...",
        "error": "⚠️ பிழை ஏற்பட்டது",
        "query_24k": "{city} இல் தற்போதைய 24K தங்க விலை என்ன?",
        "query_silver": "{city} இல் தற்போதைய வெள்ளி விலை என்ன?",
        "query_predict": "{city} இல் நாளைய 24K தங்க விலையை கணிக்கவும்",
        "query_historical": "{city} இல் கடந்த 10 நாட்களின் 24K தங்க விலைகளைக் காட்டு"
    }
}

def get_text(lang, key, **kwargs):
    """Get translated text for the given language and key"""
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
