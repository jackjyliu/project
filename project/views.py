from project import app
#from flask import render_template
from project.dashboard.plotly_test import plotly_test

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/test')
def test():
    return plotly_test()