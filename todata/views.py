from todata import app
from flask import render_template
from todata.pages.data_story_power.plotly_graph import month_hour_heatmap, monthly_power_use

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data_story_power')
def test():
    return render_template('data_story_power.html',
                            graph_1=month_hour_heatmap(),
                            graph_2=monthly_power_use())