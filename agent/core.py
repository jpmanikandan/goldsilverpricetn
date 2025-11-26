import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Import the tools we created
try:
    from tools.scraper import get_current_prices_trichy, get_historical_prices
    from tools.predictor import predict_tomorrow_price
except ImportError:
    # Fallback for when running from a different context if needed
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from tools.scraper import get_current_prices_trichy, get_historical_prices
    from tools.predictor import predict_tomorrow_price

def get_agent_executor(city: str = "Trichy"):
    """
    Initializes and returns the AgentExecutor with the Gold/Silver Price tools.
    Args:
        city: The city name for price queries (default: "Trichy")
    """
    # 1. Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # 2. Define Tools - bind city to tools
    from functools import partial
    
    # Create city-specific versions of the tools
    tools = [
        get_current_prices_trichy,
        get_historical_prices,
        predict_tomorrow_price
    ]

    # 3. Define Prompt with city context
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a helpful assistant that can:
1. Fetch current prices for 24K gold, 22K gold, 18K gold, and silver in {city}
2. Show historical prices for the last 10 days (specify metal: 24K, 22K, 18K, or Silver)
3. Predict tomorrow's price based on historical trends (specify metal: 24K, 22K, 18K, or Silver)

The user has selected {city} as their city. All price queries should be for {city}.
When users ask about prices without specifying a city, use {city}.
When asked about predictions, use the prediction tool with the appropriate metal parameter.
Always explain the methodology when providing predictions.

IMPORTANT: The tools fetch data for the city mentioned in the user's query. 
Extract the city name from queries like "[City: Chennai] show gold price" and use that city."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 4. Create Agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # 5. Create Executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor
