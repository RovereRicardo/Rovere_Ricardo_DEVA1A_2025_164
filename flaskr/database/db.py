import pymysql
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration unique qui fonctionne en local ET dans Docker
DB_HOST = os.getenv("DB_HOST", os.getenv("HOST_MYSQL", "localhost"))
DB_USER = os.getenv("DB_USER", os.getenv("USER_MYSQL", "root"))
DB_PASSWORD = os.getenv("DB_PASSWORD", os.getenv("PASS_MYSQL", "root"))
DB_PORT = int(os.getenv("DB_PORT", os.getenv("PORT_MYSQL", 3306)))
DB_NAME = os.getenv("DB_NAME", os.getenv("NAME_BD_MYSQL", "basketstats"))
DUMP_FILE_PATH = os.getenv("NAME_FILE_DUMP_SQL_BD", "flaskr/database/rovere_ricardo_deva1a_basketstats_164_2025.sql")

# Conversion du chemin du dump
absolute_dump_path = os.path.abspath(DUMP_FILE_PATH)
print(f"Absolute path to dump file: {absolute_dump_path}")


def get_db_connection():
    """Crée une connexion à la base de données MySQL"""
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def import_dump():
    """Importe le dump SQL"""
    print(f"Connexion à MySQL: host={DB_HOST}, port={DB_PORT}, user={DB_USER}, database={DB_NAME}")

    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4'
    )

    try:
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS `{DB_NAME}`;")
        print(f"Tentative de création de la base de données '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;")
        connection.commit()
        print(f"La base de données '{DB_NAME}' a été créée ou existe déjà.")
    except Exception as e:
        print(f"Erreur dans la création de la base de données '{DB_NAME}': {e}")
        cursor.close()
        connection.close()
        return

    try:
        print(f"Tentative de sélection de la base de données '{DB_NAME}'...")
        connection.select_db(DB_NAME)
        print(f"Base de données sélectionnée '{DB_NAME}'.")
    except Exception as e:
        print(f"Erreur lors de la sélection de la base de données '{DB_NAME}': {e}")
        connection.close()
        return

    if os.path.exists(absolute_dump_path):
        print(f"Fichier de sauvegarde trouvé à l'emplacement {absolute_dump_path}. Début de l'importation...")
        with open(absolute_dump_path, 'r') as dump_file:
            sql = dump_file.read()

            # Remove 'CREATE DATABASE' and 'USE <database>' statements
            sql = sql.replace(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;", "")
            sql = sql.replace(f"USE `{DB_NAME}`;", "")

            cursor = connection.cursor()

            try:
                statements = sql.split(';')
                for i, statement in enumerate(statements):
                    if statement.strip():
                        cursor.execute(statement)

                connection.commit()
                print(f"La sauvegarde de la base de données depuis {absolute_dump_path} a été importée avec succès.")
            except Exception as e:
                print(f"Erreur lors de l'importation de la sauvegarde : {e}")
                connection.rollback()
            finally:
                cursor.close()
    else:
        print(f"Le fichier de sauvegarde {absolute_dump_path} n'existe pas.")

    connection.close()


# Import au démarrage seulement
import_dump()

# Connexion globale pour l'application
connection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)
