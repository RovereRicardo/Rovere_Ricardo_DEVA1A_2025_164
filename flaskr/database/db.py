import pymysql
import os
from dotenv import load_dotenv

# chargement des variables de environment
load_dotenv()

# Fetch database config depuis les variables de environnement
HOST_MYSQL = os.getenv("HOST_MYSQL")
USER_MYSQL = os.getenv("USER_MYSQL")
PASS_MYSQL = os.getenv("PASS_MYSQL")
PORT_MYSQL = int(os.getenv("PORT_MYSQL", 3306))
DATABASE_NAME = os.getenv("NAME_BD_MYSQL")
DUMP_FILE_PATH = os.getenv("NAME_FILE_DUMP_SQL_BD")

# conversion du patch du dump
absolute_dump_path = os.path.abspath(DUMP_FILE_PATH)
print(f"Absolute path to dump file: {absolute_dump_path}")

def import_dump():
    # connection pour faire l import du dump
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
        cursor.execute(f"DROP DATABASE`{DATABASE_NAME}`;")
        print(f"Tentative de création de la base de données '{DATABASE_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}`;")
        connection.commit()
        print(f"La base de données '{DATABASE_NAME}' a été créée ou existe déjà.")
    except Exception as e:
        print(f"Erreur dans la creation de la base de données '{DATABASE_NAME}': {e}")
        cursor.close()
        connection.close()
        return


    try:
        print(f"Tentative de sélection de la base de données '{DATABASE_NAME}'...")
        connection.select_db(DATABASE_NAME)
        print(f"Base de données sélectionnée '{DATABASE_NAME}'.")
    except Exception as e:
        print(f"Erreur lors de la sélection de la base de données '{DATABASE_NAME}': {e}")
        connection.close()
        return

    if os.path.exists(absolute_dump_path):
        print(f"Fichier de sauvegarde trouvé à l'emplacement {absolute_dump_path}. Début de l'importation...")
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
                print(f"La sauvegarde de la base de données depuis {absolute_dump_path} a été importée avec succès.")
            except Exception as e:
                print(f"Erreur lors de la l'importation de la sauvegarde : {e}")
                connection.rollback()
            finally:
                cursor.close()
    else:
        print(f"Le fichier de sauvegarde {absolute_dump_path} n'existe pas.")

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