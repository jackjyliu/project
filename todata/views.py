from todata import app
from flask import render_template
from todata.pages.data_story_power.plotly_plots import daily_power_usage, day_hour_heatmap, seasonal_power_usage

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data_story_power')
def test():
    return render_template('data_story_power.html',
                            graph_1=day_hour_heatmap(),
                            graph_2=daily_power_usage(),
                            graph_3=seasonal_power_usage())