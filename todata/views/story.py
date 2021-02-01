from todata import app, cache
from flask import render_template

from todata.visuals.story.power.plots import (
    daily_power_usage,
    day_hour_heatmap,
    temperature_scatter
)


@app.route("/story/power")
@cache.cached(timeout=60)
def story_power():
    return render_template(
        "story/power.html",
        graph_1=daily_power_usage(),
        graph_2=temperature_scatter(),
        graph_3=day_hour_heatmap()
    )