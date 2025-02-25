from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskr.models.players import Player
from flaskr.models.teams import Team

player = Blueprint('player', __name__)

@player.route('/players/register_player', methods=['GET', 'POST'])
def register_player():
    if request.method == 'POST':
        name = request.form['name']
        family_name = request.form['family_name']
        number = request.form['number']  # Make sure this is a string or integer
        position = request.form['position']
        position_name = request.form['position_name']
        height = request.form['height']
        birthday = request.form['birthday']
        nationality = request.form['nationality']

        team_id = request.args.get('id_team')

        picture = request.files.get('picture')
        if picture:
            picture_data = picture.read()  # Read the file content as binary data
        else:
            picture_data = None  # If no picture is uploaded, set to None

        if not name:
            flash('Player name is required.', 'danger')
            return redirect(url_for('player.register_player'))


        new_player = Player(name, family_name, picture_data, number, position, position_name, height, birthday, nationality)
        new_player.register_player(team_id)  # Call register function
        flash("Player registered successfully.", "success")
        return redirect(url_for('index'))

    return render_template('/players/register_player.html')

@player.route('/delete_player', methods=['POST'])
def delete_player():
    id_player = request.form.get('id_player')
    id_team = request.form.get('id_team')

    if not id_player or not id_team:
        flash("Invalid player or team ID.", "danger")
        return redirect(url_for('index'))

    try:
        Player.delete_player(id_player, id_team)  # Call the delete function
        flash("Player deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting player: {str(e)}", "danger")

    return redirect(url_for('team.view_team', team_id=id_team))

@player.route('/update_player', methods=['POST', 'GET'])
def update_player():
    player_id = request.args.get('player_id', type=int)  # Get player_id from query string/link
    id_team = request.args.get('team_id', type=int)  # Get team_id from query string/link

    if not player_id:
        flash("Player ID is missing.", "danger")
        return redirect(url_for('player.register_player'))

    player_data = Player.get_by_id(player_id)

    if not player_data:
        flash("Player does not exist.", "danger")
        return redirect(url_for('player.register_player'))

    player = Player(**player_data) # Convert data to Player object

    team = None
    if id_team:
        team_data = Team.get_by_id(id_team)
        if team_data:
            team = Team(**team_data)  # Convert data to Team object

    # Team data needed to render template

    if request.method == 'POST':
        player.name = request.form['name']
        player.family_name = request.form['family_name']
        player.number = request.form['number']
        player.position = request.form['position']
        player.position_name = request.form['position_name']
        player.height = request.form['height']
        player.birthday = request.form['birthday']
        player.nationality = request.form['nationality']

        player.update_player()
        flash("Player updated successfully.", "success")
        return redirect(url_for('team.view_team', team_id=id_team))

    return render_template("players/update_player.html", player=player, team=team)

@player.route('/view_player', methods=['GET', 'POST'])
def view_player():
    player_id = request.args.get('player_id', type=int)
    id_team = request.args.get('team_id', type=int)

    team = None
    if id_team:
        team_data = Team.get_by_id(id_team)
        if team_data:
            team = Team(**team_data)  # Convert data to Team object

    if not player_id:
        flash("Player ID is missing.", "danger")
        return redirect(url_for('team.view_team', team_id=id_team))

    player_data = Player.get_by_id(player_id)
    if not player_data:
        flash("Player does not exist.", "danger")
        return redirect(url_for('team.view_team', team_id=id_team))

    player = Player(**player_data)

    return render_template("players/view_player.html", player=player, team_id=id_team, team=team)

