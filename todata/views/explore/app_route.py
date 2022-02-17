from todata import app, cache
from flask import render_template
from todata.views.explore.indicators import indicator_notes

from todata.views.explore.trails.trail_map import toronto_trails
from todata.views.explore.trails.conditions import next_two_days
from todata.views.explore.trails.trail_notes import TRAIL_NOTES

from todata.views.explore.indicators.line_plot import time_series_generator, simple_line_plot, yoy_line_plot, indexed_line_plot
from todata.views.explore.indicators.indicator_notes import INDICATOR_NOTES

from todata.views.explore.hoods.hood_map import hood_map

@app.route("/explore/trails")
@cache.cached(timeout=3600)
def explore_trails():
    return render_template(
        "explore/trails.html",
        toronto_trails=toronto_trails(),
        next_two_days=next_two_days(),
        trail_notes=TRAIL_NOTES
    )

@app.route("/explore/indicators")
@cache.cached(timeout=86400)
def indicators():
    ts = time_series_generator()

    return render_template(
        "explore/indicators.html",
        simple_line_plot=simple_line_plot(ts),
        indexed_line_plot=indexed_line_plot(ts),
        yoy_line_plot=yoy_line_plot(ts),
        indicator_notes=INDICATOR_NOTES
    )

@app.route("/explore/neighbourhoods")
@cache.cached(timeout=86400)
def hoods():
    return render_template(
        "explore/hoods.html",
        hood_map_1=hood_map(),
        hood_map_2=hood_map(),
    )