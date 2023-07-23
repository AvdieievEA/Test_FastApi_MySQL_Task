import mysql.connector
from db.models import Base
from connection import session, engine
from db_func import fill_db

username = 'root'
password = 'root'
host = 'localhost'
port = '3306'

connection = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    port=port
)

cursor = connection.cursor()
database_name = 'test_api_db'

create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
cursor.execute(create_database_query)
cursor.close()
connection.close()


Base.metadata.create_all(engine)
# Парсер для заповнення бд інфою з .csv файлів з папки db/raw_data
# fill_db()
session.commit()
session.close()

