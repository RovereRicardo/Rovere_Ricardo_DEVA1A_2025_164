import os
import base64
from flask import Flask, render_template, session, flash
from flask_login import LoginManager, current_user

from flaskr.database.db import connection, import_dump
from datetime import timedelta
from flask_bootstrap import Bootstrap5
from flaskr.models.matchs import Matchs
from flaskr.models.players import Player
from flaskr.models.stats import Stats
from flaskr.models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY= os.getenv("SECRET_KEY"),
        DATABASE=os.getenv("NAME_BD_MYSQL"),
    )

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    bootstrap = Bootstrap5(app)

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['SESSION_PERMANENT'] = True

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    @app.route("/")
    def index():

        global connection
        if not connection.open:
            connection.ping(reconnect=True)

        db_name = os.getenv("NAME_BD_MYSQL")
        connection.select_db(db_name)

        print(current_user.get_id())
        return render_template("index.html")

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