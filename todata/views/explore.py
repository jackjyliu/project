from todata import app, cache
from flask import render_template

from todata.visuals.explore.trails.trail_map import toronto_trails
from todata.visuals.explore.trails.conditions import current_condition, next_two_days


@app.route("/explore/trails")
@cache.cached(timeout=60)
def explore_trails():
    return render_template(
        "explore/trails.html",
        toronto_trails=toronto_trails(),
        current_condition=current_condition(),
        next_two_days=next_two_days(),
    )