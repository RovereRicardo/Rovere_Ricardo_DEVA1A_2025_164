import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch database configuration from environment variables
HOST_MYSQL = os.getenv("HOST_MYSQL")
USER_MYSQL = os.getenv("USER_MYSQL")
PASS_MYSQL = os.getenv("PASS_MYSQL")
PORT_MYSQL = int(os.getenv("PORT_MYSQL", 3306))
DATABASE_NAME = os.getenv("NAME_BD_MYSQL")
DUMP_FILE_PATH = os.getenv("NAME_FILE_DUMP_SQL_BD")

# Convert relative path to an absolute path
absolute_dump_path = os.path.abspath(DUMP_FILE_PATH)
print(f"Absolute path to dump file: {absolute_dump_path}")



# Function to create the database

def import_dump():
    # Establish a new connection to MySQL to run the import
    print("Importing dump...")
    connection = pymysql.connect(
        host=HOST_MYSQL,
        port=PORT_MYSQL,
        user=USER_MYSQL,
        passwd=PASS_MYSQL,
    )

    # TODO: Uncomment for development
    try:
        cursor = connection.cursor()
        print(f"Attempting to create database '{DATABASE_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}`;")
        connection.commit()
        print(f"Database '{DATABASE_NAME}' created or already exists.")
    except Exception as e:
        print(f"Error creating database '{DATABASE_NAME}': {e}")
        cursor.close()
        connection.close()
        return


    try:
        print(f"Attempting to select database '{DATABASE_NAME}'...")
        connection.select_db(DATABASE_NAME)
        print(f"Selected database '{DATABASE_NAME}'.")
    except Exception as e:
        print(f"Error selecting database '{DATABASE_NAME}': {e}")
        connection.close()
        return

    if os.path.exists(absolute_dump_path):
        print(f"Dump file found at {absolute_dump_path}. Starting import...")
        with open(absolute_dump_path, 'r') as dump_file:
            sql = dump_file.read()

            # Remove 'CREATE DATABASE' and 'USE <database>' statements
            sql = sql.replace(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}`;", "")
            sql = sql.replace(f"USE `{DATABASE_NAME}`;", "")

            cursor = connection.cursor()

            try:
                statements = sql.split(';')
                for i, statement in enumerate(statements):
                    if statement.strip():
                        cursor.execute(statement)

                connection.commit()
                print(f"Database dump from {absolute_dump_path} imported successfully.")
            except Exception as e:
                print(f"Error importing dump: {e}")
                connection.rollback()
            finally:
                cursor.close()
    else:
        print(f"Dump file {absolute_dump_path} does not exist.")

    connection.close()

import_dump()

# Establish connection to the MySQL server
connection = pymysql.connect(
    host=HOST_MYSQL,
    port=PORT_MYSQL,
    user=USER_MYSQL,
    passwd=PASS_MYSQL,
    database=DATABASE_NAME,
)