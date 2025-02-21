import os
from flask import Flask, redirect, url_for, render_template, session, request
from flaskr.db import connection  # Use 'flaskr.db' instead of 'db'
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

    @app.route("/index")
    def hello():
        return redirect(url_for('index'))

    @app.route("/")
    def index():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM t_match")
        matches = cursor.fetchall()

        cursor.execute("SELECT * FROM t_team")
        teams = cursor.fetchall()  # Fetch all results

        # Get column names from the cursor
        column_names = [desc[0] for desc in cursor.description]

        # Convert each row from tuple to dictionary
        teams = [dict(zip(column_names, team)) for team in teams]

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
        column_names = [desc[0] for desc in cursor.description]
        team = dict(zip(column_names, team))

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


    app.secret_key = os.urandom(24)

    from flaskr.auth import auth
    app.register_blueprint(auth)

    from flaskr.controller.teams import team
    app.register_blueprint(team)  # URL prefix is /teams

    from flaskr.controller.players import player
    app.register_blueprint(player)  # Ensure it's prefixed

    return app
