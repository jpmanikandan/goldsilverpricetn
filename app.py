import streamlit as st
import os
from dotenv import load_dotenv
from agent.core import get_agent_executor
from langchain_core.messages import HumanMessage, AIMessage
import base64
from translations import get_text

# Load environment variables
load_dotenv()

def get_base64_image(image_path):
    """Convert image to base64 for HTML embedding"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(
    page_title="Gold & Silver Price Prediction by BellLabs",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Header styling */
    h1 {
        background: linear-gradient(120deg, #FFD700, #FFA500, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
    }
    
    /* Circular logo */
    .circular-logo {
        border-radius: 50%;
        width: 100px;
        height: 100px;
        object-fit: cover;
        border: 4px solid #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
        to { box-shadow: 0 0 30px rgba(255, 215, 0, 0.8); }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f3460 0%, #16213e 100%);
        border-right: 2px solid #FFD700;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.2);
        backdrop-filter: blur(10px);
        margin: 10px 0;
    }
    
    /* Input box */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 25px;
        border: 2px solid #FFD700;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(120deg, #FFD700, #FFA500);
        color: #1a1a2e;
        font-weight: 600;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
    }
    
    /* Select box */
    .stSelectbox {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Fix dropdown text visibility */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }
    
    .stSelectbox label {
        color: #FFD700 !important;
        font-weight: 600;
    }
    
    /* Dropdown menu items */
    [data-baseweb="select"] > div {
        background-color: #16213e !important;
        color: #ffffff !important;
    }
    
    /* Selected option in dropdown */
    [data-baseweb="select"] input {
        color: #FFD700 !important;
    }
    
    /* Dropdown options */
    [role="option"] {
        background-color: #16213e !important;
        color: #ffffff !important;
    }
    
    [role="option"]:hover {
        background-color: rgba(255, 215, 0, 0.2) !important;
    }
    
    /* Caption */
    .caption-text {
        color: #b8b8b8;
        font-size: 16px;
        font-weight: 300;
    }
    
    /* Brand footer */
    .brand-footer {
        text-align: center;
        padding: 20px;
        background: linear-gradient(120deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        font-size: 18px;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([4, 1])
with col1:
    lang = st.session_state.get("language", "en")
    st.title(get_text(lang, "title"))
    st.markdown(f'<p class="caption-text">{get_text(lang, "subtitle")}</p>', unsafe_allow_html=True)
with col2:
    if os.path.exists("assets/belllabs_logo.jpg"):
        st.markdown(
            f'<img src="data:image/jpeg;base64,{get_base64_image("assets/belllabs_logo.jpg")}" class="circular-logo">',
            unsafe_allow_html=True
        )

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    
    # Language selector
    languages = {
        "English": "en",
        "தமிழ் (Tamil)": "ta"
    }
    selected_lang_name = st.selectbox("🌐 Language", list(languages.keys()), index=0)
    selected_lang = languages[selected_lang_name]
    
    # Store in session state
    if "language" not in st.session_state:
        st.session_state.language = selected_lang
    elif st.session_state.language != selected_lang:
        st.session_state.language = selected_lang
    
    st.markdown("---")
    
    # City selector with custom styling
    cities = [
        "Chennai", "Trichy", "Madurai", "Salem", "Coimbatore",
        "Vellore", "Tirunelveli", "Erode", "Namakkal", "Thanjavur"
    ]
    selected_city = st.selectbox(get_text(selected_lang, "select_city"), cities, index=1)
    
    # Store in session state
    if "city" not in st.session_state or st.session_state.city != selected_city:
        st.session_state.city = selected_city
        st.session_state.messages = []
    
    st.markdown("---")
    
    # Feature highlights with clickable buttons
    st.markdown(f"### {get_text(selected_lang, 'features')}")
    
    # 24K Gold button
    if st.button(get_text(selected_lang, "gold_24k"), use_container_width=True, key="gold_24k"):
        city = st.session_state.get("city", "Trichy")
        st.session_state.feature_query = get_text(selected_lang, "query_24k", city=city)
    
    # Silver button
    if st.button(get_text(selected_lang, "silver"), use_container_width=True, key="silver"):
        city = st.session_state.get("city", "Trichy")
        st.session_state.feature_query = get_text(selected_lang, "query_silver", city=city)
    
    # AI Predictions button
    if st.button(get_text(selected_lang, "predictions"), use_container_width=True, key="predictions"):
        city = st.session_state.get("city", "Trichy")
        st.session_state.feature_query = get_text(selected_lang, "query_predict", city=city)
    
    # Historical Data button
    if st.button(get_text(selected_lang, "historical"), use_container_width=True, key="historical"):
        city = st.session_state.get("city", "Trichy")
        st.session_state.feature_query = get_text(selected_lang, "query_historical", city=city)
    
    st.markdown("---")
    st.markdown(f'<div class="brand-footer">{get_text(selected_lang, "brand_footer")}</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant", avatar="💰"):
            st.markdown(message.content)

# Process feature button query if exists
if "feature_query" in st.session_state and st.session_state.feature_query:
    prompt = st.session_state.feature_query
    st.session_state.feature_query = None  # Clear it
    
    # Add to messages and process
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant", avatar="💰"):
        message_placeholder = st.empty()
        
        try:
            city = st.session_state.get("city", "Trichy")
            city_aware_prompt = f"[City: {city}] {prompt}"
            
            agent_executor = get_agent_executor(city)
            response = agent_executor.invoke({"input": city_aware_prompt})
            result = response["output"]
            
            message_placeholder.markdown(result)
            st.session_state.messages.append(AIMessage(content=result))
            
        except Exception as e:
            error_msg = f"⚠️ An error occurred: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append(AIMessage(content=error_msg))

# Chat input
lang = st.session_state.get("language", "en")
if prompt := st.chat_input(get_text(lang, "chat_placeholder")):
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant", avatar="💰"):
        message_placeholder = st.empty()
        
        try:
            city = st.session_state.get("city", "Trichy")
            city_aware_prompt = f"[City: {city}] {prompt}"
            
            agent_executor = get_agent_executor(city)
            response = agent_executor.invoke({"input": city_aware_prompt})
            result = response["output"]
            
            message_placeholder.markdown(result)
            st.session_state.messages.append(AIMessage(content=result))
            
        except Exception as e:
            error_msg = f"⚠️ An error occurred: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append(AIMessage(content=error_msg))
