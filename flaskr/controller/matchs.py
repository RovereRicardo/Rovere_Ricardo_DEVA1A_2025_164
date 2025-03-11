from flask import Blueprint, render_template, request, redirect, url_for, flash

from flaskr.WTForms.RegistrationForm import RegisterMatchForm, DeleteMatchForm, EditMatchForm
from flaskr.controller.players import player
from flaskr.database.db import connection
from flaskr.models.matchs import Matchs
from flaskr.models.players import Player
from flaskr.models.teams import Team
from flaskr.models.stats import Stats
from flaskr.models.total import Total

match = Blueprint('match', __name__)


@match.route('/matchs/register_match', methods=['GET', 'POST'])
def register_match():
    form = RegisterMatchForm(request.form)
    cursor = connection.cursor()
    cursor.execute('SELECT id_team, team_name FROM t_team')
    teams = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    teams = [dict(zip(column_names, team)) for team in teams]

    form.id_home_team.choices = form.id_away_team.choices = [(str(team['id_team']), team['team_name']) for team in
                                                             teams]
    if request.method == 'POST' and form.validate():
        if not form.id_home_team.data or not form.id_away_team.data:
            flash("Teams required.", "danger")
            return redirect(url_for('match.register_match'))

        new_match = Matchs(None, form.date.data, form.id_home_team.data, form.id_away_team.data, None, None, None, None)
        new_match.register_match()

        flash("Match Registered!", "success")
        return redirect(url_for('index'))
    return render_template('/matchs/register_match.html', teams=teams, form=form)



@match.route('/matchs/delete_match', methods=['POST'])
def delete_match():
    form = DeleteMatchForm(request.form)
    if not form.id_match.data:
        flash("Match does not exist.", "danger")
        redirect(url_for('index'))

    try:
        match_data = Matchs.get_by_id(form.id_match.data)
        if not match_data:
            flash("Match does not exist.", "danger")
            return redirect(url_for('index'))

        match = Matchs(**match_data)
        match.delete_match()
        flash("Match Deleted!", "success")
    except Exception as e:
        flash(f"Error deleting match: {str(e)}", "danger")
    return redirect(url_for('index', form=form))

@match.route('/edit_match/<int:id_match>', methods=['GET', 'POST'])
def edit_match(id_match):
    form = EditMatchForm(request.form)
    match_data = Matchs.get_match_by_id(id_match)

    cursor = connection.cursor()
    cursor.execute('SELECT id_team, team_name FROM t_team')
    teams = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    teams = [dict(zip(column_names, team)) for team in teams]

    # Assign teams to choices
    form.id_home_team.choices = form.id_away_team.choices =  [(str(team['id_team']), team['team_name']) for team in teams]

    if not match_data:
        flash("Match does not exist.", "danger")
        return redirect(url_for('index'))

    match = Matchs(**match_data)
    print("Home Team ID:", match_data['id_home_team'])
    print("Away Team ID:", match_data['id_away_team'])

    if request.method == 'GET':
        form.date_match.data = match.date_match
        form.id_home_team.data = str(match.id_home_team)
        form.id_away_team.data = str(match.id_away_team)
        form.home_score.data = match.home_score
        form.away_score.data = match.away_score

    if request.method == 'POST' and form.validate():
        match.date_match = form.date_match.data
        match.id_home_team = form.id_home_team.data
        match.id_away_team = form.id_away_team.data
        match.home_score = form.home_score.data
        match.away_score = form.away_score.data

        match.edit_match()
        flash("Match Edited!", "success")
        return redirect(url_for('index'))

    return render_template("/matchs/edit_match.html", match=match, teams=teams, form=form)


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

    players_playing = Matchs.get_players_playing(match.id_match, match.id_home_team)
    players_playing_away = Matchs.get_players_playing(match.id_match, match.id_away_team)
    print(players_playing)
    print(players_playing_away)

    return render_template('matchs/view_match.html', Total=Total, Stats=Stats, match=match, home_players=home_players,
                           away_players=away_players, players_playing=players_playing,
                           players_playing_away=players_playing_away)


@match.route('/view_match_table_ajax', methods=['GET', 'POST'])
def view_match_table_ajax():
    id_player = request.form.get('idPlayer')
    id_team = request.form.get('idTeam')
    id_match = request.form.get('idMatch')
    stat_type = request.form.get('statType')
    stat_value = request.form.get('statValue')

    stat_type_id = Stats.get_stats_by_name(stat_type)

    if stat_type_id:
        # Create a Stats instance and register it
        new_stat = Stats(stat_type_id, id_player, id_match, stat_value)
        new_stat.register_stat()

    id_match = request.args.get('id_match')

    players = Matchs.get_players_playing(id_match, id_team)
    # print(players)

    return render_template('matchs/_match_table.html', Total=Total, Stats=Stats, match_id=id_match, players=players,
                           team_id=id_team)
