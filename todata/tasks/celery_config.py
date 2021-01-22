"""
holds celery config files
"""
from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'America/Toronto'
CELERYBEAT_SCHEDULE = {  
    'hourly_load': {
        'task': 'tasks.hourly_load',
        'schedule': crontab(minute=0)
    },
    'daily_load': {
        'task': 'tasks.daily_load',
        'schedule': crontab(hour=6, minute=15)
    },
    'three_daily_load': {
        'task': 'tasks.three_daily_load',
        'schedule': crontab(hour=[7,15,23], minute=15),
    },
    'weekly_load': {
        'task': 'tasks.weekly_load',
        'schedule': crontab(day_of_week=2, hour=4, minute=15)
    }
}