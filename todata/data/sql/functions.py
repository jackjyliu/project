"""
functions to load data into postgresql database
"""
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from todata.data.credentials import WSL2_PSQL as psql

class sql:

    # init psql with defaults
    def __init__(
        self,
        database,
        user=psql["user"],
        password=psql["password"],
        host=psql["host"],
        port=psql["port"]):

        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        try:
            self.connection = psycopg2.connect(
                user=self.user, password=self.password, host=self.host, port=self.port, database=self.database
            )
            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.Error) as error:
            if self.connection:
                print(error)

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def read(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
    def read_pd(self, query):
        sql_result = pd.read_sql(query, con=self.connection)
        return sql_result

    def write(self, query, records):
        execute_batch(self.cursor, query, records)
        self.connection.commit()
        return self.cursor.rowcount

    def write_single(self, query, records):
        self.cursor.execute(query, records)
        self.connection.commit()
        return self.cursor.rowcount


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