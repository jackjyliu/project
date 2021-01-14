from todata import app
from flask import render_template
from todata.pages.sample.plotly_graph import month_hour_heatmap

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sample')
def test():
    return render_template('sample.html', graph_1=month_hour_heatmap())