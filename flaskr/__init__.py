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
        # Ensure the correct database is selected
        db_name = os.getenv("NAME_BD_MYSQL")
        connection.select_db(db_name)

        try:
            # First cursor for matches
            cursorM = connection.cursor()
            cursorM.execute("""
                SELECT 
                    m.id_match, m.id_home_team, m.id_away_team, 
                    home_team.team_name AS home_team, 
                    away_team.team_name AS away_team, 
                    m.date_match, m.home_score, m.away_score 
                FROM t_match m 
                JOIN t_team home_team ON m.id_home_team = home_team.id_team 
                JOIN t_team away_team ON m.id_away_team = away_team.id_team 
                WHERE m.is_deleted = 0
                ORDER BY m.date_match ASC
            """)
            matches = cursorM.fetchall()
            column_namesM = [desc[0] for desc in cursorM.description]
            cursorM.close()

            # Second cursor for teams
            cursorT = connection.cursor()
            cursorT.execute("SELECT * FROM t_team WHERE is_deleted = 0")
            teams = cursorT.fetchall()
            column_namesT = [desc[0] for desc in cursorT.description]
            cursorT.close()

            # Convert tuples to dictionaries
            matches = [dict(zip(column_namesM, match)) for match in matches]
            teams = [dict(zip(column_namesT, team)) for team in teams]

            username = session.get('username')  # Get username from session

            return render_template("index.html", matches=matches, teams=teams, username=username)

        except pymysql.MySQLError as e:
            return f"Database error: {str(e)}", 500


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
