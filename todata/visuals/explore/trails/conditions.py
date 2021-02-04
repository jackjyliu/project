import pandas as pd
from datetime import datetime
import pytz
from todata.models.sql.functions import sql_read_pd, sql_read

import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import todata.visuals.custom_theme
pio.templates.default = "simple_white+custom"


def condition():
    return NotImplementedError


def current_condition():
    # based on past temps and preciptation
    # plot past 5/7 days condition
    past_weather = sql_read_pd("toronto",
                        """
                        SELECT * 
                        FROM (SELECT ts, temp_c, rain_mm
                            FROM weather_temperature
                            WHERE temp_c IS NOT NULL
                            ORDER BY ts DESC
                            LIMIT 168) as last_week_weather
                        ORDER BY ts ASC
                        """)
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Temperature', 'Precipitation'))
    fig.add_trace(go.Scatter(x=past_weather.ts, y=past_weather.temp_c), row=1, col=1)
    fig.add_trace(go.Scatter(x=past_weather.ts, y=past_weather.rain_mm), row=2, col=1)
    fig.update_layout(showlegend=False, hovermode=False, margin={"r": 0, "l": 0, "b": 0})
    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    # description
    # colour code?

    return plot # return dictionary of summary + plot

def next_two_days():

    # plot of next two days of weather condition + sunrise/set
    current_weather = sql_read("toronto",
                        """
                        SELECT result 
                        FROM weather_open_api
                        WHERE data_type = 'weather'
                        ORDER BY ts DESC
                        LIMIT 1
                        """)[0][0]

    local_timezone = pytz.timezone("America/Toronto")

    # turn weather forecast into pandas df
    fct_dt = []
    temp = []
    precip = []
    wind = []
    humidity = []
    uvi = []

    for hour in current_weather['hourly']:

        utc_datetime = datetime.fromtimestamp(hour['dt'])  
        local_datetime = utc_datetime.replace(tzinfo=pytz.utc)

        fct_dt.append(local_datetime)
        temp.append(round(hour['temp'] - 273.15, 1))
        precip.append(hour['pop'])
        wind.append(round(hour['wind_speed'] * 3.6, 0))
        humidity.append(hour['humidity'])
        uvi.append(hour['uvi'])

    forecast_raw = {
        'ts': fct_dt,
        'temp': temp,
        'precip': precip,
        'wind': wind,
        'humidity': humidity,
        'uvi': uvi
    }

    forecast = pd.DataFrame(forecast_raw)
    
    # create plot
    fig = make_subplots(rows=2, cols=2, subplot_titles=('Temperature', 'Wind', 'Precipitation', 'Sun Strength'),)
    fig.add_trace(go.Scatter(x=forecast.ts, y=forecast.temp), row=1, col=1)
    fig.add_trace(go.Scatter(x=forecast.ts, y=forecast.wind), row=1, col=2)
    fig.add_trace(go.Scatter(x=forecast.ts, y=forecast.precip), row=2, col=1)
    fig.add_trace(go.Scatter(x=forecast.ts, y=forecast.uvi), row=2, col=2)
    fig.update_layout(showlegend=False, hovermode=False, margin={"r": 0, "l": 0, "b": 0})
    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    # description
    # colour code?

    return plot # return dictionary of summary + plot