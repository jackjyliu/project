"""
displays mapbox data with plotly
"""
import plotly.express as px
import plotly.io as pio
from todata.models.credentials import MAPBOX_API_KEY

import pandas as pd
import requests
from todata.models.utils.datetime import utc_to_local_time, current_local_time
from datetime import datetime, timedelta, timezone
import pytz

def road_closure_api():
    try:
        # OpenWeather One Call API
        api_call = "https://secure.toronto.ca/opendata/cart/road_restrictions.json?v=2.0"
        response = requests.get(api_call)
        response.raise_for_status()

        # convert json to dictionary
        return response.json()

    except Exception as ex:
        raise ex


def road_closure_data(api_data=road_closure_api()):

    road_pd = pd.DataFrame(api_data['Closure'])
    road_close = road_pd[['id', 'road', 'latitude', 'longitude', 'startTime', 'endTime', 'description', 'type']]
    road_close['startTime'] = road_close['startTime'].astype('int').apply(lambda x: utc_to_local_time(x/1000))
    road_close['endTime'] = road_close['endTime'].astype('int').apply(lambda x: utc_to_local_time(x/1000))
    road_close['latitude'] = road_close['latitude'].astype(float)
    road_close['longitude'] = road_close['longitude'].astype(float)
    
    two_hr_before = current_local_time() + timedelta(hours=-2)
    one_day_after = current_local_time() + timedelta(hours=24)

    active_closure = road_close[(road_close['endTime'] > two_hr_before) & (road_close['startTime'] < one_day_after)]

    return active_closure


def road_closure_map(active_closure=road_closure_data()):

    px.set_mapbox_access_token(MAPBOX_API_KEY)
    fig = px.scatter_mapbox(active_closure,
                            lat=active_closure.latitude,
                            lon=active_closure.longitude,
                            hover_name="road",
                            hover_data={
                                'StartTime': active_closure['startTime'].apply(lambda x: datetime.strftime(x,"%y.%m.%d %H:%M")),
                                'EndTime': active_closure['endTime'].apply(lambda x: datetime.strftime(x,"%y.%m.%d %H:%M")),
                                'type': True,
                                'latitude': False,
                                'longitude': False
                                },
                            mapbox_style='carto-positron',
                            zoom=9)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    plot = pio.to_html(fig, full_html=False, config={'displayModeBar':False})

    return plot