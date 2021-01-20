"""
GET current weather and pollution data from Open Weather API
default location = toronto
"""

import requests
from todata.models.credentials import WEATHER_API_KEY

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


def dashboard_weather():
    
    # load current + forecast weather from api
    w = current_weather()
    
    # select parts of weather file
    dw = {
        'current':
            {
                'weather': w['current']['weather'][0]['description'],  
                'temp_c': round(w['current']['temp'] - 273.15,1),
                'wind_speed_kmh': round(w['current']['wind_speed'] * 3.6),       
            },
        'next_hour':
            {
                'weather': w['hourly'][1]['weather'][0]['description'],  
                'temp_c': round(w['hourly'][1]['temp'] - 273.15, 1),
                'wind_speed_kmh': round(w['hourly'][1]['wind_speed'] * 3.6),
                'PoP': round(w['hourly'][1]['pop'] * 100)         
            },
        'next_day':
            {
                'weather': w['daily'][1]['weather'][0]['description'],  
                'max_temp_c': round(w['daily'][1]['temp']['max'] - 273.15, 1),
                'min_temp_c': round(w['daily'][1]['temp']['min'] - 273.15, 1),
                'wind_speed_kmh': round(w['daily'][1]['wind_speed'] * 3.6),
                'PoP': round(w['daily'][1]['pop'] * 100)        
            }        
        } 

    return dw