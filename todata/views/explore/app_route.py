from todata import app, cache
from flask import render_template

from todata.views.explore.trails.trail_map import toronto_trails
from todata.views.explore.trails.conditions import next_two_days
from todata.views.explore.trails.trail_notes import TRAIL_NOTES


@app.route("/explore/trails")
#@cache.cached(timeout=60)
def explore_trails():
    return render_template(
        "explore/trails.html",
        toronto_trails=toronto_trails(),
        next_two_days=next_two_days(),
        trail_notes=TRAIL_NOTES
    )