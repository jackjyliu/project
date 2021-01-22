"""
main file which runs the flask app
import other components into this file
"""

from flask import Flask
from flask_caching import Cache
from celery import Celery
import todata.tasks.celery_config as celery_config


app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

celery = Celery(app.name, broker=celery_config.CELERY_BROKER_URL)
celery.config_from_object(celery_config)

import todata.tasks.celery_tasks

import todata.views

if __name__ == "__main__":
    app.run()