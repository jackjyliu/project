from todata import app
from flask import render_template
from todata.pages.data_story_power.plotly_plots import daily_power_usage, day_hour_heatmap, seasonal_power_usage
from todata.models.api.bing_news import bing_news as news_api
from todata.models.api.open_weather import dashboard_weather
from datetime import datetime


@app.route('/')
@app.route('/dashboard')
def dashboard():
    # current date and time
    current_time = datetime.now()
    toronto_time = current_time.strftime("%Y/%m/%d %H:%M")
    
    local_news = news_api()

    dw = dashboard_weather()

    return render_template('dashboard.html',
                            toronto_time=toronto_time,
                            local_news=local_news,
                            dw=dw)

@app.route('/data_story_power')
def data_story_power():
    return render_template('data_story_power.html',
                            graph_1=day_hour_heatmap(),
                            graph_2=daily_power_usage(),
                            graph_3=seasonal_power_usage())