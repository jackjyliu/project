"""
displays mapbox data with plotly
"""
import plotly.express as px
import plotly.io as pio
import todata.views.plotly_custom_theme
from todata.data.credentials import MAPBOX_API_KEY

import pandas as pd
import requests
from todata.data.utils.datetime import utc_to_local_time, current_local_time
from datetime import datetime, timedelta, timezone

pio.templates.default = "simple_white+custom"
pd.set_option("mode.chained_assignment", None)

def road_closure_api():
    """
    get live toronto road closure data from api,
    return python dictionary
    """
    try:
        # OpenWeather One Call API
        api_call = "https://secure.toronto.ca/opendata/cart/road_restrictions.json?v=2.0"
        response = requests.get(api_call)
        response.raise_for_status()

        # convert json to dictionary
        return response.json()

    except Exception as ex:
        raise ex


def road_closure_map(api_data=road_closure_api()):
    """
    input road closure api data as pandas dictionary and returns plotly map with recent road closure locations
    """
    road_pd = pd.DataFrame(api_data['Closure'])
    road_close = road_pd[['id', 'road', 'latitude', 'longitude', 'startTime', 'endTime', 'description', 'type']]
    road_close = road_close[road_close['type'] == 'HAZARD']
    road_close = road_close[~road_close['description'].str.contains('CafeTO')]
    road_close['startTime'] = road_close['startTime'].astype('int').apply(lambda x: utc_to_local_time(x/1000))
    road_close['endTime'] = road_close['endTime'].astype('int').apply(lambda x: utc_to_local_time(x/1000))
    road_close['latitude'] = road_close['latitude'].astype(float)
    road_close['longitude'] = road_close['longitude'].astype(float)
    
    two_hr_before = current_local_time() + timedelta(hours=-2)
    one_day_after = current_local_time() + timedelta(hours=24)

    active_closure = road_close[(road_close['endTime'] > two_hr_before) & (road_close['startTime'] < one_day_after)]
    
    active_closure['description'] = active_closure['description'].str.wrap(40)
    active_closure['description'] = active_closure['description'].apply(lambda x: x.replace('\n', '<br>'))

    px.set_mapbox_access_token(MAPBOX_API_KEY)
    fig = px.scatter_mapbox(active_closure,
                            lat=active_closure.latitude,
                            lon=active_closure.longitude,
                            hover_name="road",
                            hover_data={
                                'StartTime': active_closure['startTime'].apply(lambda x: datetime.strftime(x,"%y.%m.%d %H:%M")),
                                'EndTime': active_closure['endTime'].apply(lambda x: datetime.strftime(x,"%y.%m.%d %H:%M")),
                                'description': True,
                                'latitude': False,
                                'longitude': False
                                },
                            mapbox_style='carto-positron',
                            zoom=9)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    plot = pio.to_html(fig, full_html=False, config={'displayModeBar':False})

    return plot