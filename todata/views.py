from todata import app, cache
from flask import render_template
from datetime import datetime

from todata.pages.dashboard.news_psql import latest_news
from todata.pages.dashboard.weather_live import dashboard_weather

from todata.pages.data_story_power.plotly_plots import daily_power_usage, day_hour_heatmap, seasonal_power_usage


@app.route('/')
@app.route('/dashboard')
@cache.cached(timeout=60)
def dashboard():
    # current date and time
    current_time = datetime.now()
    toronto_time = current_time.strftime("%Y/%m/%d %H:%M")

    return render_template('dashboard.html',
                            toronto_time=toronto_time,
                            local_news=latest_news(),
                            dw=dashboard_weather())

@app.route('/data_story_power')
@cache.cached(timeout=3600)
def data_story_power():
    return render_template('data_story_power.html',
                            graph_1=day_hour_heatmap(),
                            graph_2=daily_power_usage(),
                            graph_3=seasonal_power_usage())