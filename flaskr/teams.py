import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.db import connection

team = Blueprint('team', __name__)


# Team Registration
@team.route('/teams/register_team', methods=['GET', 'POST'])
def register_team():
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_logo = request.form['team_logo']
        address = request.form['address']
        city = request.form['city']
        wins = request.form['wins']
        loses = request.form['loses']
        draws = request.form['draws']
        points = request.form['points']
        id_user = session.get('id_user')

        if not team_name:
            flash("Team Name is required.", "danger")
            return redirect(url_for('team.register_team'))

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO t_team (team_name, team_logo, address, city, wins, loses, draws, points,id_coach_creator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (team_name, team_logo, address, city, wins, loses, draws, points, id_user))
        connection.commit()
        cursor.close()

        flash("Team Registered!", "success")
        return redirect(url_for('index'))
    return render_template('/teams/register_team.html')


@team.route('/teams/delete_team', methods=['POST'])
def delete_team():
    if request.method == 'POST':
        team_id = request.form['id_team']
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM t_team WHERE id_team = %s",
            (team_id,)  # Ensure it's a tuple
        )
        connection.commit()
        cursor.close()
        flash("Team Deleted!", "success")
        return redirect(url_for('index'))


@team.route('/update/<int:team_id>', methods=('GET', 'POST'))
def update_team(team_id):
    cursor = connection.cursor()

    if request.method == 'POST':
        team_name = request.form['team_name']
        team_logo = request.form['team_logo']
        address = request.form['address']
        city = request.form['city']
        wins = request.form['wins']
        loses = request.form['loses']
        draws = request.form['draws']
        points = request.form['points']

        error = None

        if not team_name:
            error = 'Team name is required.'

        if error is not None:
            flash(error)
        else:
            cursor.execute(
                'UPDATE t_team SET team_name = %s, team_logo = %s, address = %s, city = %s, wins = %s, loses = %s, draws = %s, points = %s WHERE id_team = %s',
                (team_name, team_logo, address, city, wins, loses, draws, points, team_id)
            )
            connection.commit()
            flash('Team updated successfully!', 'success')
            return redirect(url_for('index'))

    cursor.execute(
        'SELECT * FROM t_team WHERE id_team = %s',
        (team_id,)
    )
    team = cursor.fetchone()
    team = dict(zip([desc[0] for desc in cursor.description], team))

    return render_template('teams/update_team.html', team=team)

@team.route('view_team/<int:team_id>', methods=('GET', 'POST'))
def view_team(team_id):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM t_team WHERE id_team = %s',
        (team_id,)
    )
    team = cursor.fetchone()
    team = dict(zip([desc[0] for desc in cursor.description], team))
    return render_template('teams/view_team.html', team=team)
