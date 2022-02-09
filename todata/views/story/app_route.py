from numpy import mintypecode
from todata import app, cache
from flask import render_template

from todata.views.story.power.plots import (
    daily_power_usage,
    day_hour_heatmap,
    temperature_scatter,
    temp_effect
)

from todata.views.story.bike.plots import (
    daily_trips,
    minute_trips,
    month_map,
    hour_map,
    net_flow_map
)


@app.route("/story/power")
#@cache.cached(timeout=3600)
def story_power():
    return render_template(
        "story/power.html",
        daily_power_usage=daily_power_usage(),
        temperature_scatter=temperature_scatter(),
        day_hour_heatmap=day_hour_heatmap(),
        temp_effect = temp_effect()
    )

@app.route("/story/bike")
#@cache.cached(timeout=3600)
def story_bike():
    return render_template(
        "story/bike.html",
        daily_trips=daily_trips(),
        minute_trips=minute_trips(),
        month_map=month_map(),
        hour_map=hour_map(),
        net_flow_map=net_flow_map(),
    )