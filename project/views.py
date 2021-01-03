from project import app
from flask import render_template
from project.dashboard.plotly_graph import plotly_test

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('plotly_graph.html', graph=plotly_test())