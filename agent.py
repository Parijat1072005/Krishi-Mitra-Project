# File: agent.py

import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.agents import tool, AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
# --- THIS IMPORT IS UPDATED ---
from langchain_chroma import Chroma

# Import our actual data fetching functions
from data_fetchers import fetch_weather_data, fetch_mandi_price_data

# Define the path to the persisted vector database
PERSIST_DIRECTORY = "db"
# Initialize the embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# Load the persisted database from disk
vector_db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)

# 1. Define the Tools the Agent can use

@tool
def get_weather_forecast(location: str) -> str:
    """Finds the current weather forecast for a given location in India."""
    print(f"TOOL USED: Getting weather for {location}")
    return fetch_weather_data(city_name=location)

@tool
def get_market_price(market: str, crop: str) -> str:
    """Gets the most recent modal price for a crop at a specific mandi/market."""
    print(f"TOOL USED: Getting price for {crop} in {market}")
    return fetch_mandi_price_data(market=market, commodity=crop)

@tool
def find_government_scheme(query: str) -> str:
    """
    Searches the knowledge base for relevant government schemes, subsidies, or farming advisories from downloaded documents.
    Use this for questions about financial support, policies, or specific crop advice found in PDFs.
    """
    print(f"TOOL USED: Searching knowledge base for: '{query}'")
    results = vector_db.similarity_search(query, k=2)
    
    if not results:
        return "I could not find any relevant information in the knowledge base."
    
    response_text = "Based on the knowledge base, here's what I found:\n"
    for i, doc in enumerate(results):
        source_file = os.path.basename(doc.metadata.get('source', 'Unknown'))
        response_text += f"\n--- From Document: {source_file} ---\n"
        response_text += doc.page_content + "\n"
        
    return response_text

# 2. Set up the LLM Agent
def create_agent():
    """Creates and returns the AI agent executor."""
    # --- LET'S SWITCH TO A MORE QUOTA-FRIENDLY MODEL FOR NOW ---
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
    
    tools = [get_weather_forecast, get_market_price, find_government_scheme]

    prompt_template = """
    You are Krishi-Mitra, a helpful AI assistant for Indian farmers.
    Answer the user's question based on the data provided by the tools.
    Be concise and helpful. When using information from the knowledge base, mention it.
    You must determine all required parameters for a tool from the user's query.
    Today's date is August 10, 2025.

    User question: {input}
    Agent scratchpad: {agent_scratchpad}
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_template),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor