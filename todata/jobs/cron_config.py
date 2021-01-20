"""
config crontab to run different jobs at different time periods
"""

from crontab import CronTab

cron = CronTab(user='jliu')

daily_job = cron.new(command='/home/jliu/project/test-venv/bin/python /home/jliu/project/todata/models/jobs/daily_sql_load.py') # TODO fix module not found when file is run from terminal
daily_job.hour.on(3)
cron.write()