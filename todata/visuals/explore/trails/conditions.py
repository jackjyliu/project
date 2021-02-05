import pandas as pd
from datetime import datetime, timezone
import pytz
from todata.models.sql.functions import sql_read_pd, sql_read

import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import todata.visuals.custom_theme
pio.templates.default = "simple_white+custom"

def utc_to_local_time(utc_raw):
    """
    convert utc datetime string to toronto time
    """
    local_timezone = pytz.timezone("America/Toronto")
    utc_datetime = datetime.fromtimestamp(utc_raw, tz=timezone.utc)  
    local_datetime = utc_datetime.astimezone(local_timezone)

    return local_datetime


def past_weather():
    """
    return past weeks temperature and rain as dataframe
    """
    past_weather = sql_read_pd("toronto",
                        """
                        SELECT * 
                        FROM (SELECT ts, temp_c AS temp, rain_mm AS precip
                            FROM weather_temperature
                            WHERE temp_c IS NOT NULL
                            ORDER BY ts DESC
                            LIMIT 168) as last_week_weather
                        ORDER BY ts ASC
                        """)
    return past_weather


def weather_forecast():
    """
    return 48 hr forecast as pandas dataframe 
    """
    current_weather = sql_read("toronto",
                        """
                        SELECT result 
                        FROM weather_open_api
                        WHERE data_type = 'weather'
                        ORDER BY ts DESC
                        LIMIT 1
                        """)[0][0]

    # turn weather forecast into pandas df
    fct_dt = []
    temp = []
    precip = []
    wind = []
    humidity = []
    uvi = []
    clouds = []

    for hour in current_weather['hourly']:

        fct_dt.append(utc_to_local_time(hour['dt']))
        temp.append(round(hour['temp'] - 273.15, 1))
        precip.append(hour['pop'])
        wind.append(round(hour['wind_speed'] * 3.6, 0))
        humidity.append(hour['humidity'])
        uvi.append(hour['uvi'])
        clouds.append(hour['clouds'])

    forecast_raw = {
        'ts': fct_dt,
        'temp': temp,
        'precip': precip,
        'wind': wind,
        'humidity': humidity,
        'uvi': uvi,
        'clouds': clouds
    }

    forecast = pd.DataFrame(forecast_raw)

    # get sunrise/set and convert to toronto timezone
    sunrise = utc_to_local_time(current_weather['current']['sunrise'])
    sunset = utc_to_local_time(current_weather['current']['sunset'])

    forecast_package = {
        'forecast': forecast,
        'sunrise': sunrise,
        'sunset': sunset
    }

    return forecast_package


def condition_check(past_weather=past_weather(), weather_forecast=weather_forecast()):
    """
    return condition of trails based on temperature, precipitation, wind, etc
    """
    
    # calculate past weather variables

    past = past_weather.sort_values(by=['ts'], ascending=False).head(36)
    past_avg_temp = past['temp'].mean()
    past_is_rain = past['precip'].sum() > 1
    past_is_ice = past_avg_temp < 1

    # calculate future weather variables
    weather = weather_forecast['forecast']
    avg_temp = weather['temp'].mean()
    is_rain = weather['precip'].sum() > 1
    is_windy = weather['wind'].mean() > 30
    is_humid = weather['humidity'].mean() > 60 and avg_temp > 21
        
    # calculate temp warnings
    is_hot = avg_temp > 25
    is_cold = avg_temp < 10
    is_ice = avg_temp < 1

    # add mosquito warning
    month = weather['ts'].min().month
    is_mosquito = month > 5 and month < 10

    # accumulate score and description for output
    score = 0
    description = ""

    # add to description
    if is_hot: description = description + ", hot day"
    if is_rain: description = description + ", precipiation"
    if is_ice or past_is_ice: description = description + ", icy conditions"
    else:
        if is_cold: description = description + ", chilly day"
        if is_rain or past_is_rain: description = description + ", wet or muddy ground"
    if is_windy: description = description + ", windy"
    if is_humid: description = description + ", high humidity"
    if is_mosquito: description = description + ", potential mosquitos"

    # string strip
    description = description.strip(" ,")

    return description


def next_two_days():

    # plot of next two days of weather condition + sunrise/set
    forecast_raw = weather_forecast()
    forecast = forecast_raw['forecast']
       
    # create plot
    fig = make_subplots(rows=2, cols=2, subplot_titles=('Temperature C', 'Wind Km/h', 'Precipitation %', 'Sun Strength'),)
    fig.add_trace(go.Scatter(x=forecast.ts, y=forecast.temp), row=1, col=1)
    fig.add_trace(go.Scatter(x=forecast.ts, y=forecast.wind), row=1, col=2)
    fig.add_trace(go.Scatter(x=forecast.ts, y=forecast.precip), row=2, col=1)
    fig.add_trace(go.Scatter(x=forecast.ts, y=forecast.uvi), row=2, col=2)
    fig.update_layout(showlegend=False, hovermode=False, margin={"r": 0, "l": 0, "b": 0})
    plot = pio.to_html(fig, full_html=False, config={"displayModeBar": False})

    plot_pkg = {
        'plot': plot,
        'sunrise': forecast_raw['sunrise'].strftime("%H:%M"),
        'sunset': forecast_raw['sunset'].strftime("%H:%M"),
        'condition': condition_check()
    }

    return plot_pkg # return dictionary of summary + plot