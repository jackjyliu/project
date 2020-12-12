"""
functions to load data into postgresql database
"""
from datetime import datetime
import data_toronto
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import sql_login as psql
from datetime import datetime

def sql_write(user, password, host, port, database, query, records):
    
    # connect to database
    try: 
        connection = psycopg2.connect(user=psql.user,
                                        password=psql.password,
                                        host=psql.host,
                                        port=psql.port,
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
            return True

def update_toronto_power():
    """
    insert toronto power data for rows not in already in database 
    """
    connection = psycopg2.connect(user=psql.user,
                                    password=psql.password,
                                    host=psql.host,
                                    port=psql.port,
                                    database='toronto')
    cursor = connection.cursor()


    # get last inserted timestamp
    last_record = pd.read_sql('SELECT ts FROM power WHERE power_use_mwh IS NOT NULL ORDER BY ts DESC LIMIT 1'
                            ,con=connection)
    
    last_ts = last_record['ts'][0]

    # filter records to only new data
    power_data = data_toronto.toronto_power(start_year=max(2004,last_ts.year))
    new_power_data = power_data[power_data['ts'] > last_ts]
    new_power_data = new_power_data.where(pd.notnull(new_power_data), None)
    
    write_db = 'toronto'
    query = 'INSERT INTO power (ts, power_use_mwh) VALUES (%s, %s);'
    records = [tuple(x) for x in new_power_data.to_numpy()]

    sql_write(psql.user, psql.password, psql.host, psql.port, write_db, query, records)
    
    cursor.close()
    connection.close()
    #print('toronto power load complete')
    return True

def update_toronto_temp():
    """
    insert latest toronto temperature data
    """

    connection = psycopg2.connect(user=psql.user,
                                    password=psql.password,
                                    host=psql.host,
                                    port=psql.port,
                                    database='toronto')
    cursor = connection.cursor()


    # get last inserted timestamp
    last_record = pd.read_sql('SELECT ts FROM weather WHERE temp_c IS NOT NULL ORDER BY ts DESC LIMIT 1'
                            ,con=connection)
    
    last_ts = last_record['ts'][0]

    # filter records to only new data
    weather_data = data_toronto.toronto_weather(start_year=max(2004,last_ts.year))
    new_weather_data = weather_data[weather_data['ts'] > last_ts]
    new_weather_data = new_weather_data.where(pd.notnull(new_weather_data), None)

    write_db = 'toronto'
    query = """ 
                INSERT INTO weather (ts, temp_c, rel_hum_pct, pressure_kpa) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (ts) DO UPDATE
                    SET 
                        temp_c = excluded.temp_c,
                        rel_hum_pct = excluded.rel_hum_pct,
                        pressure_kpa = excluded.pressure_kpa;
            """
    records = [tuple(x) for x in new_weather_data.to_numpy()]

    sql_write(psql.user, psql.password, psql.host, psql.port, write_db, query, records)
    
    cursor.close()
    connection.close()
    return True