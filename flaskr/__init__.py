import os
import base64

import pymysql
from flask import Flask, redirect, url_for, render_template, session, request
from flaskr.database.db import connection, import_dump
from datetime import timedelta
from flask_bootstrap import Bootstrap5

from flaskr.models.matchs import Matchs
from flaskr.models.players import Player
from flaskr.models.stats import Stats

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.getenv("NAME_BD_MYSQL"),
    )

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['SESSION_PERMANENT'] = True

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    @app.route("/")
    def index():
        # Ensure the connection is open
        global connection
        if not connection.open:
            connection.ping(reconnect=True)

        # Ensure the correct database is selected
        db_name = os.getenv("NAME_BD_MYSQL")
        connection.select_db(db_name)

        username = session.get('username')  # Get username from session

        return render_template("index.html", username=username)

    @app.template_filter('b64encode')
    def b64encode_filter(data):
        return base64.b64encode(data).decode('utf-8') if data else None

    app.secret_key = os.urandom(24)

    from flaskr.controller.user import user
    app.register_blueprint(user)

    from flaskr.controller.teams import team
    app.register_blueprint(team)

    from flaskr.controller.players import player
    app.register_blueprint(player)

    from flaskr.controller.matchs import match
    app.register_blueprint(match)

    from flaskr.controller.stats import stat
    app.register_blueprint(stat)

    return app
