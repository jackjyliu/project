from todata import app, cache
from flask import render_template
from datetime import datetime
import pytz

from todata.pages.dashboard.news_psql import latest_news
from todata.pages.dashboard.weather_live import dashboard_weather
from todata.pages.dashboard.mapbox import points_of_interest

from todata.pages.data_story_power.plotly_plots import (
    daily_power_usage,
    day_hour_heatmap,
    temperature_scatter
)


@app.route("/")
@app.route("/dashboard")
@cache.cached(timeout=60)
def dashboard():
    
    tz = pytz.timezone('America/Toronto')
    toronto_time = datetime.now(tz).strftime("%Y/%m/%d %H:%M")

    return render_template(
        "dashboard.html",
        toronto_time=toronto_time,
        local_news=latest_news(),
        dw=dashboard_weather(),
        points_of_interest=points_of_interest(),
    )


@app.route("/data_story_power")
@cache.cached(timeout=60)
def data_story_power():
    return render_template(
        "data_story_power.html",
        graph_1=daily_power_usage(),
        graph_2=temperature_scatter(),
        graph_3=day_hour_heatmap()
    )

@app.route("/about")
@cache.cached(timeout=1)
def about():
    return render_template("about.html")