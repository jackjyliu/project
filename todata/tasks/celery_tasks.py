"""
celery tasks to pass to main __init__ flask function
"""
import celery

import todata.data.toronto.update as to
import todata.data.api.update as api


@celery.task(name="tasks.hourly_load")
def hourly_load():
    api.update_weather()
    api.update_pollution()
    return True


@celery.task(name="tasks.daily_load")
def daily_load():
    to.update_toronto_power()
    to.update_toronto_temp()
    return True


@celery.task(name="tasks.three_daily_load")
def three_daily_load():
    api.update_news()
    return True


@celery.task(name="tasks.weekly_load")
def weekly_load():
    to.update_business_licence()
    api.update_statcan()
    return True