import psycopg2
from psycopg2 import Error
import os

def setup_database():
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="your_password",
            database="postgres"
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("DROP DATABASE IF EXISTS final_proje_v1")
        cursor.execute("CREATE DATABASE final_proje_v1")
        
        connection.close()
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="your_password",
            database="final_proje_v1"
        )
        cursor = connection.cursor()

        with open('db/database_schema.sql', 'r', encoding='utf-8') as schema_file:
            cursor.execute(schema_file.read())

        with open('db/initial_data.sql', 'r', encoding='utf-8') as data_file:
            cursor.execute(data_file.read())

        connection.commit()
        print("Database created and initialized successfully!")

    except (Exception, Error) as error:
        print(f"Error occurred: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_database()