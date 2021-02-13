import pandas as pd
import plotly.express as px
import plotly.io as pio
from todata.data.credentials import MAPBOX_API_KEY


def toronto_trails():

    trails = pd.read_csv("./todata/data/files/maps/trails.csv")

    px.set_mapbox_access_token(MAPBOX_API_KEY)
    fig = px.line_mapbox(trails,
        lat=trails.lat,
        lon=trails.lon,
        hover_name=trails.names,
        hover_data={
            'lat': False,
            'lon': False
        },
        mapbox_style="carto-positron",
        zoom=9,
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    return plot