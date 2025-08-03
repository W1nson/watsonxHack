
from langchain_core.tools import tool

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