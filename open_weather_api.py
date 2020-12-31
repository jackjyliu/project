"""
GET current weather and pollution data from Open Weather API
default location = toronto
"""

import requests
from credentials import weather_api_key

TORONTO_LAT = '43.6533'
TORONTO_LONG = '-79.3841'

def weather(lat=TORONTO_LAT, lon=TORONTO_LONG, part='', api_key=weather_api_key):
    
    # OpenWeather One Call API
    api_call = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}"
    response = requests.get(api_call)

    # convert json to dictionary
    response_json = response.json()
    return response_json


def pollution(lat=TORONTO_LAT, lon=TORONTO_LONG, api_key=weather_api_key):

    # OpenWeather Pollution API
    api_call = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(api_call)

    # convert json to dictionary
    response_json = response.json()
    return response_json