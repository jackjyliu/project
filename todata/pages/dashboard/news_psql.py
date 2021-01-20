"""
pull the latest bing news record from psql database and convert to list of dictionaries for dashboard
"""

from todata.models.sql.functions import sql_read


def latest_news():

    # read latest news as json from psql database
    news = sql_read('toronto','SELECT result FROM bing_news ORDER BY ts DESC LIMIT 1')

    return news[0][0]