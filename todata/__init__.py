"""
main file which runs the flask app
import other components into this file
"""

from flask import Flask
from flask_caching import Cache
from celery import Celery
from celery.schedules import crontab

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERYBEAT_SCHEDULE'] = {  
    'hourly_load': {
        'task': 'tasks.hourly_load',
        'schedule': crontab(minute=0)
    },
    'daily_load': {
        'task': 'tasks.daily_load',
        'schedule': crontab(hour=6, minute=15)
    },
    'weekly_load': {
        'task': 'tasks.weekly_load',
        'schedule': crontab(day_of_week=2, hour=4, minute=15)
    }
}
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

import todata.tasks.celery_tasks

import todata.views

if __name__ == "__main__":
    app.run()