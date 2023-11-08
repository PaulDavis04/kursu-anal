import pandas as pd

import matplotlib.pyplot as plt
import psycopg2
import requests
from bs4 import BeautifulSoup
###------------------

import psycopg2
from psycopg2 import sql

from scraping import currency_scraping

def connect_db():
    conn_params = {
        'dbname': 'Valiutu_kursai',
        'user': 'postgres',
        'password': 'Litovic',
        'host': 'localhost'
    }
    return conn_params

def create_database(dbname, user, password, host, port, new_dbname):
    conn_params = {
        "database": dbname,
        "user": user,
        "password": password,
        "host": host,
        "port": port
    }
    # Establish a connection to the database
    try:
        connection= psycopg2.connect(**conn_params)
        connection.autocommit= True
        cursor = connection.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE{}").format(sql.Identifier(new_dbname)))
        print(f"database {new_dbname} created succesfuly")

        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        print(f"An Error occured while creating the database {e}")

# create_database("postgres", 'postgres','Litovic', 'localhost', 5432,'Valiutu_kursai')

def create_and_insert_currency(conn_params, table_name, columns):
    connection = psycopg2.connect(**conn_params)
    connection.autocommit = True
    cursor = connection.cursor()

    try:
        # Drop the table if it exists
        drop_table_query =sql.SQL("DROP TABLE IF EXISTS {}").format(
            sql.Identifier(table_name))

        cursor.execute(drop_table_query)
        print(f"TABLE {table_name} DROPPED SUCCESFULY")
    except psycopg2.Error as e:
        print(f"AN ERROR OCCURED WHILE DROPPING THE TABLE{e}")
    try :
        columns_with_types = ', '.join([f"{col_name} {data_type}" for col_name, data_type in columns.items()])
        create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(columns_with_types)
        )

        # Execute the create table query
        cursor.execute(create_table_query)
        print(f"Table {table_name} created successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred while creating {table_name}: {e}")
    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()

conn_params = {
    "dbname":"Valiutu_kursai",
    "user": "postgres",
    "password": "Litovic",
    "host": "localhost"
}
table_name = 'currency_rates'
columns = {
    'id': 'SERIAL PRIMARY KEY',
    'title': 'VARCHAR(100)',
    'currency_rate': 'VARCHAR(10)',
    'curr_proportion': 'DECIMAL(10,2)',
    'curr_change': 'DECIMAL(10,2)',
    'curr_change_percentage': 'DECIMAL(10,2)',
    'currency_date': 'DATE'
}


# Create table
# create_and_insert_currency(conn_params, table_name, columns)

def insert_currency_data(conn_params, data):
    # Establish a connection to the database
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    insert_stmt = """
    INSERT INTO currency_rates (currency_date, title, currency_rate, curr_proportion, curr_change, curr_change_percentage)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for row in data:
        cur.execute(insert_stmt, row)

    conn.commit()

    cur.close()
    conn.close()
    print("Data inserted successfully.")

##Uzkomentavome skreipinima
# currency_data = currency_scraping()

# insert_currency_data(conn_params, currency_data)

columns = ['currency_date', 'title', 'currency_rate', 'curr_proportion', 'curr_change', 'curr_change_percentage']


def select_currency_data(conn_params, table_name, columns=columns, conditions=None):
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    select_stmt = f"SELECT {columns} from {table_name} "

    if isinstance(columns, list):
        columns = ', '.join(columns)
        select_stmt = f"SELECT {columns} from {table_name} "

    if conditions:
        select_stmt += f"WHERE {conditions}"

    cur.execute(select_stmt)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

# table_name = 'currency_rates'
# columns = ['title', 'currency_rate', 'curr_proportion', 'curr_change', 'curr_change_percentage']
# conditions = ""
# selected_data = select_currency_data(conn_params, table_name, columns, conditions)
#
# for row in selected_data:
#     print(row)