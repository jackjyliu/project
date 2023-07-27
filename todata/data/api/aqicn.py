"""
GET current pollution data from AQICN API
default location = toronto
"""

import requests
from todata.data.credentials import AQICN_API_KEY

# default location
CITY = "toronto"

def aqicn_pollution(location=CITY, api_key=AQICN_API_KEY):
    
    try:
        # AQICN Call API
        api_call = f"https://api.waqi.info/feed/{location}/?token={api_key}"
        response = requests.get(api_call)
        response.raise_for_status()

        # convert json to dictionary
        return response.json()
    
    except Exception as ex:
        raise ex