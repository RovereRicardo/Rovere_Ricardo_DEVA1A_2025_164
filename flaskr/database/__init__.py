import os
from flask import Flask

app = Flask(__name__)

# Configuration MySQL depuis les variables d'environnement
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 3306))
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'basketstats')
