"""
displays mapbox data with plotly
"""
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
from todata.models.credentials import MAPBOX_API_KEY

def points_of_interest():
    with open('todata/models/data_files/maps/poi.geojson') as f:
        poi = gpd.read_file(f)

    px.set_mapbox_access_token(MAPBOX_API_KEY)
    fig = px.scatter_mapbox(poi,
                            lat=poi.geometry.y,
                            lon=poi.geometry.x,
                            hover_name="NAME",
                            zoom=9)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    plot = pio.to_html(fig, full_html=False)

    return plot