import os
import base64

import pymysql
from flask import Flask, redirect, url_for, render_template, session, request
from flaskr.database.db import connection, import_dump
from datetime import timedelta

from flaskr.models.matchs import Matchs
from flaskr.models.players import Player
from flaskr.models.stats import Stats


def create_app():
    app = Flask(__name__)
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
                ORDER BY m.date_match ASC
            """)
            matches = cursorM.fetchall()
            column_namesM = [desc[0] for desc in cursorM.description]
            cursorM.close()

            # Second cursor for teams
            cursorT = connection.cursor()
            cursorT.execute("SELECT * FROM t_team")
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

    @app.route("/matches/edit_match")
    def edit_match():
        username = session.get('username')
        iduser = session.get('id_user')

        return render_template("/matchs/edit_match.html", match=match, username=username, iduser=iduser)

    @app.route("/matches/view_match")
    def view_match():
        username = session.get('username')
        iduser = session.get('id_user')


        return render_template("/matchs/view_matchs.html", match=match, username=username, iduser=iduser)


    @app.route('/register_stat', methods=['POST'])
    def register_stat():
        id_player = request.form.get('idPlayer')
        id_match = request.form.get('idMatch')
        stat_type = request.form.get('statType')
        stat_value = request.form.get('statValue')

        stat_type_id = Stats.get_stats_by_name(stat_type)

        if stat_type_id:
            # Create a Stats instance and register it
            new_stat = Stats(stat_type_id, id_player, id_match, stat_value)
            new_stat.register_stat()
            return redirect(url_for('match.view_match', id_match=id_match))
        else:
            return "Error: Stat type not found", 400

    @app.route('/submit_score', methods=['POST'])
    def submit_score():
        home_team_score = request.form.get('homeTeamScore')
        away_team_score = request.form.get('awayTeamScore')
        id_home_team = request.form.get('id_home_team')
        id_away_team = request.form.get('id_away_team')
        id_match = request.form.get('idMatch')

        Matchs.submit_score(id_match, home_team_score, away_team_score)

        if home_team_score > away_team_score:
            Matchs.set_win(id_home_team)
            Matchs.set_lose(id_away_team)
        else:
            Matchs.set_win(id_away_team)
            Matchs.set_lose(id_home_team)

        return redirect(url_for('match.view_match', id_match=id_match))

    @app.route('/add_player_home', methods=['POST'])
    def add_player_home():
        id_player = request.form.get('idPlayerHome')
        id_match = request.form.get('id_match')
        Matchs.add_player_to_mach(id_match, id_player)

        return redirect(url_for('match.view_match', id_match=id_match))

    @app.route('/add_player_away', methods=['POST'])
    def add_player_away():
        id_player = request.form.get('idPlayerAway')
        id_match = request.form.get('id_match')
        Matchs.add_player_to_mach(id_match, id_player)

        return redirect(url_for('match.view_match', id_match=id_match))


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
