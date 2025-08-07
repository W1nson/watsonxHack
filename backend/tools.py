
from langchain_core.tools import tool
import requests 
import json
from datetime import datetime
import os 
from dotenv import load_dotenv
load_dotenv()



@tool 
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool 
def get_current_earthquake(city: str) -> str:
    """Get current earthquake for a given city."""
    return f"It's always sunny in {city}!"

@tool 
def get_current_date() -> str:
    """Get current date."""
    return datetime.now().strftime("%B %d, %Y")


@tool 
def web_search(query: str) -> dict:
    """Get web search results for a given query."""
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': os.getenv("SERPER_APIKEY"),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


