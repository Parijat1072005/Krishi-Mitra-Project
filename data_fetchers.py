import os
import requests
from dotenv import load_dotenv

# Import non-secret settings from our config file
import config

# Load environment variables from the .env file
load_dotenv()

# Securely get API keys from the environment
# The os.getenv() function reads the variables we loaded from the .env file
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
DATA_GOV_KEY = os.getenv("DATA_GOV_API_KEY")

# --- Function Definitions ---

def fetch_weather_data(city_name=config.DEFAULT_CITY):
    """Fetches real-time weather data for a given city."""
    if not OPENWEATHER_KEY:
        print("Error: OpenWeatherMap API key not found. Please set it in the .env file.")
        return

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    full_url = f"{base_url}?q={city_name},IN&appid={OPENWEATHER_KEY}&units=metric"

    try:
        response = requests.get(full_url)
        response.raise_for_status()
        data = response.json()
        
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        print(f"🌦️ Weather in {city_name.title()}: {temp}°C, {humidity}% humidity. ({description.title()})")
        return data

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error fetching weather: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")



def fetch_mandi_price_data(state=config.DEFAULT_STATE, market=config.DEFAULT_MARKET, commodity=config.DEFAULT_COMMODITY):
    """Fetches and cleans real-time market prices."""
    # ... (API key check and URL construction remain the same) ...
    if not DATA_GOV_KEY:
        print("Error: data.gov.in API key not found. Please set it in the .env file.")
        return

    # **THIS IS THE MISSING PART**
    # Define the base URL for the data.gov.in API
    base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    # Construct the full URL with the API key and filters
    full_url = (f"{base_url}?api-key={DATA_GOV_KEY}&format=json&"
                f"filters[state]={state}&filters[district]={market}&filters[commodity]={commodity}")
    
    print(f"Querying URL: {base_url}...") # Helpful for debugging

    try:
        response = requests.get(full_url)
        response.raise_for_status()
        data = response.json()
        records = data.get('records', [])

        if not records:
            print(f"💰 No market data found for {commodity} in {market}, {state}.")
            return None

        latest_record = records[0]

        # --- LIGHTWEIGHT, ON-THE-FLY CLEANING ---
        # 1. Safely convert price to a number. Default to 0.0 if it's missing or not a number.
        try:
            modal_price = float(latest_record.get('modal_price', 0))
        except (ValueError, TypeError):
            modal_price = 0.0

        # 2. Standardize text data.
        arrival_date = latest_record.get('arrival_date', 'N/A').strip()
        cleaned_commodity = latest_record.get('commodity', 'Unknown').strip()
        # --- END OF ON-THE-FLY CLEANING ---

        print(f"💰 Price for {cleaned_commodity} in {market} (as of {arrival_date}): ₹{modal_price:.2f}/Quintal.")
        
        # Return a clean, structured dictionary for other parts of your app to use
        return {
            "state": state,
            "market": market,
            "commodity": cleaned_commodity,
            "price": modal_price,
            "date": arrival_date
        }

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error fetching prices: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

