"""
functions to load data into postgresql database
"""
import data_toronto
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import sql_win_login as psql
import datetime

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

def insert_toronto_power():
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

    write_db = 'toronto'
    query = 'INSERT INTO power (ts, power_use_mwh) VALUES (%s, %s);'
    records = [tuple(x) for x in new_power_data.to_numpy()]

    sql_write(psql.user, psql.password, psql.host, psql.port, write_db, query, records)
    
    print('toronto power load complete')
    return True


