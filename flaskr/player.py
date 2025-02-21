import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.db import connection

player = Blueprint('player', __name__)

@player.route('/players/register_player', methods=['GET', 'POST'])
def register_player():
    if request.method == 'POST':
        name = request.form['name']
        family_name = request.form['family_name']
        number = request.form['number']
        position = request.form['position']
        position_name = request.form['position_name']
        height = request.form['height']
        birthday = request.form['birthday']
        nationality = request.form['nationality']


        if not name:
            flash("Name is required.", "danger")
            return redirect(url_for('player.register_player'))

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO t_player (name, family_name, number, position, position_name, height, birthday) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, family_name, number, position, position_name, height, birthday))

        connection.commit()

        cursor.execute("INSERT INTO t_team_player (id_team_player, id_player_team) VALUES (%s, %s)", (request.args.get('id_team'), cursor.lastrowid))

        connection.commit()
        cursor.close()

        flash("Player Registered!", "success")
        return redirect(url_for('index'))
    return render_template('/players/register_player.html')
