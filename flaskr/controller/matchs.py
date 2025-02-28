from flask import Blueprint, render_template, request, redirect, url_for, flash

from flaskr.database.db import connection
from flaskr.models.matchs import Matchs

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