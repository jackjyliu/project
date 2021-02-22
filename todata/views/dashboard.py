from todata import app, cache
from flask import render_template
from datetime import datetime
import pytz

from todata.visuals.dashboard.news_psql import latest_news
from todata.visuals.dashboard.weather_live import dashboard_weather
from todata.visuals.dashboard.road_closure import road_closure_map
from todata.visuals.dashboard.kpi import kpi_package

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
        road_closure=road_closure_map(),
        kpi_package = kpi_package()
    )