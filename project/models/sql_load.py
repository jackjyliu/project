"""
functions to load data into postgresql database
"""
from datetime import datetime
import project.models.data_toronto as data_toronto
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from project.models.credentials import WSL2_PSQL as psql
from datetime import datetime

def sql_read(database, query, user=psql['user'], password=psql['password'], host=psql['host'], port=psql['port']):
    
    # connect to database
    try: 
        connection = psycopg2.connect(user=user,
                                        password=password,
                                        host=host,
                                        port=port,
                                        database=database)
        cursor = connection.cursor()
        
        # run query with pandas
        sql_result = pd.read_sql(query, con=connection)
        return sql_result
    
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print(error)
    
    finally:
        if(connection):
            cursor.close()
            connection.close()


def sql_write(database, query, records, user=psql['user'], password=psql['password'], host=psql['host'], port=psql['port']):
    
    # connect to database
    try: 
        connection = psycopg2.connect(user=user,
                                        password=password,
                                        host=host,
                                        port=port,
                                        database=database)
        cursor = connection.cursor()
        
        # run query
        sql_insert_query = query
        insert_records = records
        execute_batch(cursor, sql_insert_query, insert_records)
        connection.commit()
        
        return cursor.rowcount
    
    except (Exception, psycopg2.Error) as error:
        if(connection):
            print(error)
    
    finally:
        if(connection):
            cursor.close()
            connection.close()


def update_toronto_power():
    """
    insert toronto power data for rows not in already in database 
    """

    # get last inserted timestamp
    read_query =    """
                    SELECT ts FROM power WHERE power_use_mwh IS NOT NULL ORDER BY ts DESC LIMIT 1
                    """

    last_record = sql_read('toronto', read_query)
    last_ts = last_record['ts'][0]
    
    # filter records to only new data
    power_data = data_toronto.toronto_power(start_year=max(2004,last_ts.year))
    new_power_data = power_data[power_data['ts'] > last_ts]
    new_power_data = new_power_data.where(pd.notnull(new_power_data), None)
    
    # write records into table
    write_db = 'toronto'
    query = """
                BEGIN;
                INSERT INTO power (ts, power_use_mwh) VALUES (%s, %s);
                COMMIT;
            """
    records = [tuple(x) for x in new_power_data.to_numpy()]
    sql_write(write_db, query, records)
    
    return True


def update_toronto_temp():
    """
    insert latest toronto temperature data
    """

    # get last inserted timestamp
    read_query = 'SELECT ts FROM weather WHERE temp_c IS NOT NULL ORDER BY ts DESC LIMIT 1'
    last_record = sql_read('toronto', read_query)
    last_ts = last_record['ts'][0]

    # filter records to only new data
    weather_data = data_toronto.toronto_weather(start_year=max(2004,last_ts.year))
    new_weather_data = weather_data[weather_data['ts'] > last_ts]
    new_weather_data = new_weather_data.where(pd.notnull(new_weather_data), None)

    # write records into table
    write_db = 'toronto'
    query = """ 
                BEGIN;
                INSERT INTO weather (ts, temp_c, rel_hum_pct, pressure_kpa) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (ts) DO UPDATE
                    SET 
                        temp_c = excluded.temp_c,
                        rel_hum_pct = excluded.rel_hum_pct,
                        pressure_kpa = excluded.pressure_kpa;
                COMMIT;
            """
    records = [tuple(x) for x in new_weather_data.to_numpy()]
    sql_write(write_db, query, records)
    
    return True


def update_toronto_rain():
    """
    insert latest toronto rain data
    """

    # get last inserted timestamp
    read_query = 'SELECT ts FROM rain WHERE rain_mm IS NOT NULL ORDER BY ts DESC LIMIT 1'
    last_record = sql_read('toronto', read_query)
    last_ts = last_record['ts'][0]


    # filter records to only new data
    rain_data = data_toronto.toronto_rain()
    new_rain_data = rain_data[rain_data['ts'] > last_ts]
    new_rain_data = new_rain_data.where(pd.notnull(new_rain_data), None) 

    # write records into table
    write_db = 'toronto'
    query = """ 
                BEGIN;
                INSERT INTO rain (ts, rain_mm) 
                VALUES (%s, %s)
                ON CONFLICT (ts) DO UPDATE
                    SET 
                        rain_mm = excluded.rain_mm;
                COMMIT;
            """
    records = [tuple(x) for x in new_rain_data.to_numpy()]
    sql_write(write_db, query, records)
    
    return True


def update_toronto_daylight(start_year=2000, end_year=2022):

    # load daylight data
    daylight_data = data_toronto.toronto_daylight(start_year=start_year, end_year=end_year)

    # write records into table
    write_db = 'toronto'
    query = """ 
                BEGIN;
                INSERT INTO daylight (cdate, rise, set, hours) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (cdate) DO UPDATE
                    SET 
                        cdate = excluded.cdate,
                        rise = excluded.rise,
                        set = excluded.set,
                        hours = excluded.hours;
                COMMIT;
            """
    records = [tuple(x) for x in daylight_data.to_numpy()]
    sql_write(write_db, query, records)   
    
    return True