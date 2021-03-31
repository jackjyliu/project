from todata import app, cache
from flask import render_template

from todata.views.story.power.plots import (
    daily_power_usage,
    day_hour_heatmap,
    temperature_scatter
)


@app.route("/story/power")
#@cache.cached(timeout=3600)
def story_power():
    return render_template(
        "story/power.html",
        daily_power_usage=daily_power_usage(),
        temperature_scatter=temperature_scatter(),
        day_hour_heatmap=day_hour_heatmap()
    )