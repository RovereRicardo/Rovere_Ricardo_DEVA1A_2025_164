import os
import base64
from flask import Flask, redirect, url_for, render_template, session, request
from flaskr.database.db import connection, import_dump
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=connection,
    )

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    app.config['SESSION_PERMANENT'] = True

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    import_dump()

    @app.route("/index")
    def hello():
        # Ensure the correct database is selected
        connection.select_db(os.getenv("NAME_BD_MYSQL"))

        cursorM = connection.cursor()
        cursorM.execute(
            "SELECT m.id_match, m.id_home_team, m.id_away_team, home_team.team_name AS home_team, away_team.team_name AS away_team, m.date_match, m.home_score, m.away_score FROM t_match m JOIN t_team home_team ON m.id_home_team = home_team.id_team JOIN t_team away_team ON m.id_away_team = away_team.id_team ORDER BY m.date_match ASC"
        )
        matches = cursorM.fetchall()
        cursorM.close()

        cursorT = connection.cursor()
        cursorT.execute("SELECT * FROM t_team")
        teams = cursorT.fetchall()  # Fetch all results
        cursorT.close()

        # Get column names from the cursor
        column_namesM = [desc[0] for desc in cursorM.description]
        column_namesT = [desc[0] for desc in cursorT.description]

        # Convert each row from tuple to dictionary
        teams = [dict(zip(column_namesT, team)) for team in teams]
        matches = [dict(zip(column_namesM, match)) for match in matches]

        username = session.get('username')  # Get username from session

        return render_template("index.html", matches=matches, teams=teams, username=username)

    @app.route("/")
    def index():
        # Ensure the correct database is selected
        connection.select_db(os.getenv("NAME_BD_MYSQL"))

        cursorM = connection.cursor()
        cursorM.execute(
            "SELECT m.id_match, m.id_home_team, m.id_away_team, home_team.team_name AS home_team, away_team.team_name AS away_team, m.date_match, m.home_score, m.away_score FROM t_match m JOIN t_team home_team ON m.id_home_team = home_team.id_team JOIN t_team away_team ON m.id_away_team = away_team.id_team ORDER BY m.date_match ASC"
        )
        matches = cursorM.fetchall()
        cursorM.close()

        cursorT = connection.cursor()
        cursorT.execute("SELECT * FROM t_team")
        teams = cursorT.fetchall()  # Fetch all results
        cursorT.close()

        # Get column names from the cursor
        column_namesM = [desc[0] for desc in cursorM.description]
        column_namesT = [desc[0] for desc in cursorT.description]

        # Convert each row from tuple to dictionary
        teams = [dict(zip(column_namesT, team)) for team in teams]
        matches = [dict(zip(column_namesM, match)) for match in matches]

        username = session.get('username')  # Get username from session

        return render_template("index.html", matches=matches, teams=teams, username=username)

    @app.route("/teams/register_team")
    def register_team():
        username = session.get('username')
        iduser = session.get('id_user')
        return render_template("/teams/register_team.html", username=username, iduser=iduser)

    @app.route("/teams/view_team/<int:team_id>")
    def view_team(team_id):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM t_team WHERE id_team = %s", (team_id,))
        team = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]  # Get columns names
        team = dict(zip(column_names, team))  # Convert from tuple to dictionary

        cursor.execute(
            "SELECT p.* FROM t_player p JOIN t_team_player tp ON p.id_player = tp.id_player_team JOIN t_team t ON tp.id_team_player = t.id_team WHERE t.id_team = %s",
            (team_id,))
        players = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        players = [dict(zip(column_names, player)) for player in players]

        return render_template("/teams/view_team.html", team=team, username=session.get('username'), players=players)

    @app.route("/teams/update_team/", methods=('GET', 'POST'))
    def update_team():
        username = session.get('username')
        iduser = session.get('id_user')

        return render_template('teams/update_team.html', team=team, username=username, iduser=iduser)

    @app.route("/players/register_player")
    def register_player():
        username = session.get('username')
        iduser = session.get('id_user')
        id_team = request.args.get('id_team')

        return render_template("/players/register_player.html", username=username, iduser=iduser, id_team=id_team)

    @app.route("/players/update_player")
    def update_player():
        username = session.get('username')
        iduser = session.get('id_user')
        id_team = request.args.get('id_team')

        return render_template("/players/update_player.html", username=username, iduser=iduser, team=team)

    @app.route("/players/view_player")
    def view_player():
        username = session.get('username')
        iduser = session.get('id_user')
        id_team = request.args.get('id_team')

        return render_template("/players/view_player.html", username=username, iduser=iduser, id_team=id_team)

    @app.route("/matches/register_match")
    def register_match():
        username = session.get('username')
        iduser = session.get('id_user')

        return render_template("/matchs/register_match.html", username=username, iduser=iduser)


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

    return app
