from todata.models.api.open_weather import current_weather, current_pollution
from todata.models.api.bing_news import bing_news
from todata.models.sql.functions import sql_write
import json


def update_weather():

    # call api
    weather = current_weather()

    # convert to json
    insert_weather = json.dumps(weather)

    # write records into table
    write_db = "toronto"
    query = """
                BEGIN;
                INSERT INTO weather_open_api (ts, data_type, result) VALUES (CURRENT_TIMESTAMP, %s, %s);
                COMMIT;
            """
    records = ("weather", insert_weather)
    sql_write(write_db, query, records, single_insert=True)

    return True


def update_pollution():

    # call api
    pollution = current_pollution()

    # convert to json
    insert_records = json.dumps(pollution)

    # write records into table
    write_db = "toronto"
    query = """
                BEGIN;
                INSERT INTO weather_open_api (ts, data_type, result) VALUES (CURRENT_TIMESTAMP, %s, %s);
                COMMIT;
            """
    records = ("pollution", insert_records)
    sql_write(write_db, query, records, single_insert=True)

    return True


def update_news():

    # call api
    news = bing_news()

    # convert to json
    insert_records = json.dumps(news)

    # write records into table
    write_db = "toronto"
    query = """
                BEGIN;
                INSERT INTO news_bing (ts, result) VALUES (CURRENT_TIMESTAMP, %s);
                COMMIT;
            """
    records = (insert_records,)
    sql_write(write_db, query, records, single_insert=True)

    return True