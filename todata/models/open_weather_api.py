"""
GET current weather and pollution data from Open Weather API
default location = toronto
"""

import requests
from credentials import WEATHER_API_KEY

TORONTO_LAT = '43.6533'
TORONTO_LONG = '-79.3841'

def current_weather(lat=TORONTO_LAT, lon=TORONTO_LONG, part='', api_key=WEATHER_API_KEY):
    
    try:
        # OpenWeather One Call API
        api_call = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}"
        response = requests.get(api_call)
        response.raise_for_status()

        # convert json to dictionary
        return response.json()
    
    except Exception as ex:
        raise ex


def current_pollution(lat=TORONTO_LAT, lon=TORONTO_LONG, api_key=WEATHER_API_KEY):

    try:
        # OpenWeather Pollution API
        api_call = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(api_call)
        response.raise_for_status()

        # convert json to dictionary
        return response.json()
    
    except Exception as ex:
        raise ex