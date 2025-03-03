from flask import Blueprint, render_template, request, redirect, url_for, flash

from flaskr.controller.players import player
from flaskr.database.db import connection
from flaskr.models.matchs import Matchs
from flaskr.models.players import Player
from flaskr.models.teams import Team

match = Blueprint('match', __name__)

@match.route('/matchs/register_match', methods=['GET', 'POST'])
def register_match():

    cursor = connection.cursor()
    cursor.execute('SELECT id_team, team_name FROM t_team')
    teams = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    teams = [dict(zip(column_names, team)) for team in teams]

    if request.method == 'POST':
        date = request.form['date_match']
        id_home_team = request.form['id_home_team']
        id_away_team = request.form['id_away_team']

        if not id_home_team or not id_away_team:
            flash("Teams required.", "danger")
            return redirect(url_for('match.register_match'))

        new_match = Matchs(None, date, id_home_team, id_away_team,None,None,None,None)
        new_match.register_match()

        flash("Match Registered!", "success")
        return redirect(url_for('index'))
    return render_template('/matchs/register_match.html', teams=teams)

@match.route('/matchs/delete_match', methods=['POST'])
def delete_match():
    if request.method == 'POST':
        id_match = request.form['id_match']

        match_data = Matchs.get_by_id(id_match)

        if not match_data:
            flash("Match does not exist.", "danger")
            return redirect(url_for('index'))

        match = Matchs(**match_data)
        match.delete_match()

        flash("Match Deleted!", "success")
        return redirect(url_for('index'))

@match.route('/edit_match/<int:id_match>', methods=['GET','POST'])
def edit_match(id_match):

    cursor = connection.cursor()
    cursor.execute('SELECT id_team, team_name FROM t_team')
    teams = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    teams = [dict(zip(column_names, team)) for team in teams]

    match_data = Matchs.get_by_id(id_match)

    if not match_data:
        flash("Match does not exist.", "danger")
        return redirect(url_for('index'))

    match = Matchs(**match_data)

    if request.method == 'POST':
        match.date_match = request.form['date_match']
        match.id_home_team = request.form['id_home_team']
        match.id_away_team = request.form['id_away_team']
        match.home_score = request.form['home_score']
        match.away_score = request.form['away_score']


        match.edit_match()
        flash("Match Edited!", "success")
        return redirect(url_for('index'))

    return render_template("/matchs/edit_match.html", match=match, teams=teams)

@match.route('/view_match', methods=['GET', 'POST'])
def view_match():
    id_match = request.args.get('id_match')

    match_data = Matchs.get_match_by_id(id_match)

    if not match_data:
        flash("Match does not exist.", "danger")
        return redirect(url_for('index'))

    match = Matchs(**match_data)

    home_players = Player.get_by_team(match.id_home_team)
    away_players = Player.get_by_team(match.id_away_team)

    if request.method == 'POST':
        Matchs.add_player_to_mach(match.id_match, request.form['idPlayer'])

    players_playing = Matchs.get_players_playing(match.id_match,match.id_home_team)

    return render_template('matchs/view_match.html', match=match, home_players=home_players, away_players=away_players, players_playing=players_playing)