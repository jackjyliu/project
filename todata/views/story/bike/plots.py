"""
plotly visuals for toronto bikeshare data
"""
import pandas as pd
import platform

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import todata.views.plotly_custom_theme

pio.templates.default = "simple_white+custom"


def daily_trips():
    # daily toronto bike share trips 2021
    
    daily_trips = pd.read_pickle('./todata/static/stories/bike/daily_trips.pkl')

    fig = px.line(daily_trips, x=daily_trips.index, y=daily_trips)
    fig.update_layout(
        title="Daily Trips",
        xaxis_title=None,
        yaxis_title="Trips",
        legend_title=None,
        title_x=0.5,
        showlegend=False,
        plot_bgcolor="white",
        legend=dict(x=0.05, y=1),
        margin={"r": 15, "l": 0, "b": 0}
    )
    fig.update_traces(hovertemplate='%{x} <br>Trips: %{y}')

    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot


def minute_trips():
    # toronto bike share trips 2021 by minute

    minute_trips = pd.read_pickle('./todata/static/stories/bike/minute_trips.pkl')

    fig = px.line(minute_trips, x="Start Time", y="trips", color='Weekday' )

    fig.update_layout(
        title="Trips by Minute",
        xaxis_title=None,
        yaxis_title="Trips",
        legend_title=None,
        title_x=0.5,
        showlegend=False,
        plot_bgcolor="white",
        legend=dict(x=0.05, y=1),
        margin={"r": 15, "l": 0, "b": 0},
        hovermode='x unified'
    )
    fig.update_traces(hovertemplate='%{y}')

    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot


def net_flow_map():
    # map of net flow of bike from stations

    hour_flow_merged = pd.read_pickle('./todata/static/stories/bike/net_flow.pkl')

    fig = px.scatter_mapbox(hour_flow_merged, lat="lat", lon="lon", color="Net Flow", animation_frame='hour',
                            color_continuous_midpoint=0, range_color=[-250,250], color_continuous_scale='RdYlBu', size_max=15, zoom=10,
                            hover_name="name",
                            hover_data={
                                'Start Station Id':False,
                                'hour':True,
                                'Net Flow':True,
                                'lat':False,
                                'lon':False
                            }
                            )

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot


def hour_map():

    hour_traffic_merged = pd.read_pickle('./todata/static/stories/bike/hour_map.pkl')

    fig = px.scatter_mapbox(hour_traffic_merged, lat="lat", lon="lon", size='Trip Starts', animation_frame='hour', size_max=15, zoom=10,
                        hover_name="name",
                        hover_data={
                            'Start Station Id':False,
                            'hour':True,
                            'Trip Starts':True,
                            'station_id':False,
                            'lat':False,
                            'lon':False
                        }
)

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot


def month_map():

    month_traffic_merged = pd.read_pickle('./todata/static/stories/bike/month_map.pkl')

    fig = px.scatter_mapbox(month_traffic_merged, lat="lat", lon="lon", size="Trip Starts", animation_frame='month', size_max=15, zoom=10,
                        hover_name="name",
                        hover_data={
                            'Start Station Id':False,
                            'month':True,
                            'Trip Starts':True,
                            'station_id':False,
                            'lat':False,
                            'lon':False
                        })

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    plot = pio.to_html(fig, full_html=False, auto_play=False, config={"displayModeBar": False})

    return plot