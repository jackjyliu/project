from todata import app, cache
from flask import render_template


@app.route("/about")
@cache.cached(timeout=60)
def about():
    return render_template("about.html")