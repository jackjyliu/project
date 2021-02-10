from todata import app, cache
from flask import render_template
from datetime import datetime
import pytz

from todata.visuals.dashboard.news_psql import latest_news
from todata.visuals.dashboard.weather_live import dashboard_weather
from todata.visuals.dashboard.mapbox import points_of_interest


@app.route("/")
@app.route("/dashboard")
#@cache.cached(timeout=60)
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