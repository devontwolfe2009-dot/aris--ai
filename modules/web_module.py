"""
Web Module
Handles web browsing, weather, YouTube, and other web-based operations
"""

import webbrowser
import requests
import os
from utils.logger import setup_logger

logger = setup_logger(__name__)

def get_weather(location='current'):
    """
    Get weather information for a location
    
    Args:
        location (str): Location to get weather for
    
    Returns:
        str: Weather information
    """
    try:
        api_key = os.getenv('WEATHER_API_KEY')
        if not api_key:
            logger.warning("Weather API key not configured")
            return "Weather API not configured. Please add WEATHER_API_KEY to .env"
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"Weather in {location}: {description}, Temperature: {temp}°C"
        else:
            logger.error(f"Weather API error: {data.get('message')}")
            return f"Could not get weather for {location}"
    
    except Exception as e:
        logger.error(f"Error getting weather: {str(e)}")
        return "I couldn't retrieve the weather information."

def open_youtube(query=None):
    """
    Open YouTube or search for a video
    
    Args:
        query (str): Optional search query
    """
    try:
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            logger.info(f"Searching YouTube for: {query}")
        else:
            url = "https://www.youtube.com"
            logger.info("Opening YouTube")
        
        webbrowser.open(url)
        return f"Opening YouTube" + (f" and searching for {query}" if query else "")
    
    except Exception as e:
        logger.error(f"Error opening YouTube: {str(e)}")
        return "I couldn't open YouTube."

def open_website(url):
    """
    Open a website in the default browser
    
    Args:
        url (str): Website URL
    """
    try:
        if not url.startswith('http'):
            url = f"https://{url}"
        
        logger.info(f"Opening website: {url}")
        webbrowser.open(url)
        return f"Opening {url}"
    
    except Exception as e:
        logger.error(f"Error opening website: {str(e)}")
        return "I couldn't open that website."

def search_google(query):
    """
    Search Google for a query
    
    Args:
        query (str): Search query
    """
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        logger.info(f"Searching Google for: {query}")
        webbrowser.open(url)
        return f"Searching Google for {query}"
    
    except Exception as e:
        logger.error(f"Error searching Google: {str(e)}")
        return "I couldn't perform that search."

def get_news():
    """
    Get latest news headlines
    
    Returns:
        str: News headlines
    """
    try:
        # This would require a news API key
        # For now, return a placeholder
        logger.info("Fetching news")
        return "Opening news. Please check a news website for the latest headlines."
    
    except Exception as e:
        logger.error(f"Error getting news: {str(e)}")
        return "I couldn't retrieve the news."
