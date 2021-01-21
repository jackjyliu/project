"""
main file which runs the flask app
import other components into this file
"""

from flask import Flask
from flask_caching import Cache

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

import todata.views

if __name__ == "__main__":
    app.run()