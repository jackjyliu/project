from todata import app, cache
from flask import render_template
from datetime import datetime
import pytz

from todata.views.dashboard.news_psql import latest_news
from todata.views.dashboard.weather_live import dashboard_weather
from todata.views.dashboard.road_closure import road_closure_map
from todata.views.dashboard.kpi import kpi_package
from todata.views.dashboard.calendar import CALENDAR

@cache.cached(timeout=86400, key_prefix='kpi_cache')
def kpi_view():
    return kpi_package()

@app.route("/")
@app.route("/dashboard")
#@cache.cached(timeout=60)
def dashboard():
    
    tz = pytz.timezone('America/Toronto')
    toronto_time = datetime.now(tz).strftime("%Y.%m.%d")

    local_news = latest_news()[:10]

    return render_template(
        "dashboard.html",
        toronto_time=toronto_time,
        local_news=local_news,
        dw=dashboard_weather(),
        road_closure=road_closure_map(),
        kpi_package=kpi_view(),
        local_calendar=CALENDAR,
    )