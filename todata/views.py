from todata import app, cache
from flask import render_template
from datetime import datetime
import pytz

from todata.pages.dashboard.news_psql import latest_news
from todata.pages.dashboard.weather_live import dashboard_weather
from todata.pages.dashboard.mapbox import points_of_interest

from todata.pages.story_power.plotly_plots import (
    daily_power_usage,
    day_hour_heatmap,
    temperature_scatter
)

from todata.pages.explore_trails.trail_map import toronto_trails


@app.route("/")
@app.route("/dashboard")
@cache.cached(timeout=60)
def dashboard():
    
    tz = pytz.timezone('America/Toronto')
    toronto_time = datetime.now(tz).strftime("%Y.%m.%d %H:%M")

    return render_template(
        "dashboard.html",
        toronto_time=toronto_time,
        local_news=latest_news(),
        dw=dashboard_weather(),
        points_of_interest=points_of_interest(),
    )


@app.route("/story_power")
@cache.cached(timeout=60)
def story_power():
    return render_template(
        "story_power.html",
        graph_1=daily_power_usage(),
        graph_2=temperature_scatter(),
        graph_3=day_hour_heatmap()
    )

@app.route("/explore_trails")
@cache.cached(timeout=60)
def explore_trails():
    return render_template(
        "explore_trails.html",
        toronto_trails=toronto_trails()
    )

@app.route("/about")
@cache.cached(timeout=60)
def about():
    return render_template("about.html")