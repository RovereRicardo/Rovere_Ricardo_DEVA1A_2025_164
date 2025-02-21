import pymysql

# Database connection
connection = pymysql.connect(
    host="localhost",
    port=8889,
    user="root",
    passwd="root",
    database="flask_db"
)

cursor = connection.cursor()
