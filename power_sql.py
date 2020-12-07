import pandas as pd
from sqlalchemy import create_engine
import psycopg2

db_uri = 'postgres+psycopg2://postgres:JU900391@localhost:5432/toronto'
engine = create_engine(db_uri)

db_connection = engine.connect()

db_connection.close()