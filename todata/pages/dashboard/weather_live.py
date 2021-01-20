"""
get live weather data from open weather api and format for dictionary for dashbaord
"""

from todata.models.api.open_weather import current_weather


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