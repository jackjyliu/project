"""
functions to load data into postgresql database
"""
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from todata.models.credentials import WSL2_PSQL as psql


def sql_read(
    database,
    query,
    user=psql["user"],
    password=psql["password"],
    host=psql["host"],
    port=psql["port"],
):

    # connect to database
    try:
        connection = psycopg2.connect(
            user=user, password=password, host=host, port=port, database=database
        )
        cursor = connection.cursor()

        # run SELECT query
        cursor.execute(query)
        return cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        if connection:
            print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def sql_read_pd(
    database,
    query,
    user=psql["user"],
    password=psql["password"],
    host=psql["host"],
    port=psql["port"],
):

    # connect to database
    try:
        connection = psycopg2.connect(
            user=user, password=password, host=host, port=port, database=database
        )
        cursor = connection.cursor()

        # run query with pandas
        sql_result = pd.read_sql(query, con=connection)
        return sql_result

    except (Exception, psycopg2.Error) as error:
        if connection:
            print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def sql_write(
    database,
    query,
    records,
    single_insert=False,
    user=psql["user"],
    password=psql["password"],
    host=psql["host"],
    port=psql["port"],
):

    # connect to database
    try:
        connection = psycopg2.connect(
            user=user, password=password, host=host, port=port, database=database
        )
        cursor = connection.cursor()

        # run query
        if single_insert:
            cursor.execute(query, records)
            connection.commit()

        else:
            sql_insert_query = query
            insert_records = records
            execute_batch(cursor, sql_insert_query, insert_records)
            connection.commit()

        return cursor.rowcount

    except (Exception, psycopg2.Error) as error:
        if connection:
            print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()