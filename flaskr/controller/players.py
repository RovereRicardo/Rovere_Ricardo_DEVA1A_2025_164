
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flaskr.WTForms.RegistrationForm import RegisterPlayer, EditPlayer, DeletePlayer
from flaskr.models.players import Player
from flaskr.models.teams import Team

player = Blueprint('player', __name__)

@player.route('/players/register_player', methods=['GET', 'POST'])
def register_player():
    form = RegisterPlayer(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        family_name = form.family_name.data
        picture = form.picture.data
        number = form.number.data
        position = form.position.data
        position_name = form.position_name.data
        height = form.height.data
        birthday = form.birthday.data
        nationality = form.nationality.data
        id_team = form.id_team.data

        if picture:
            picture_data = picture.read()  # Read the file content as binary data
        else:
            picture_data = None  # If no picture is uploaded, set to None

        if not name:
            flash('Player name is required.', 'danger')
            return redirect(url_for('player.register_player'))

        new_player = Player(name, family_name, picture_data, number, position, position_name, height, birthday, nationality)
        new_player.register_player(id_team)  # Call register function
        flash("Player registered successfully.", "success")
        return redirect(url_for('team.view_team', id_team=id_team, form=form))
    return render_template('/players/register_player.html')


@player.route('/delete_player', methods=['POST'])
def delete_player():
    form = DeletePlayer(request.form)
    id_player = form.id_player.data
    id_team = form.id_team.data

    if not id_player or not id_team:
        flash("Invalid player or team ID.", "danger")
        return redirect(url_for('index'))

    try:
        Player.delete_player(id_player, id_team)  # Call the delete function
        flash("Player deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting player: {str(e)}", "danger")

    return redirect(url_for('team.view_team', id_team=id_team, form=form))

@player.route('/update_player', methods=['POST', 'GET'])
def update_player():
    form = EditPlayer(request.form)
    player_id = request.args.get('player_id', type=int)  # Get player_id from query string/link
    id_team = request.args.get('id_team', type=int)  # Get team_id from query string/link

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

    if request.method == 'POST' and form.validate():
        player.name = form.name.data
        player.family_name = form.family_name.data
        player.number = form.number.data
        player.position = form.position.data
        player.position_name = form.position_name.data
        player.height = form.height.data
        player.birthday = form.birthday.data
        player.nationality = form.nationality.data

        player.update_player()
        flash("Player updated successfully.", "success")
        return redirect(url_for('team.view_team', id_team=id_team))

    return render_template("players/update_player.html", player=player, team=team, form=form)

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
        return redirect(url_for('team.view_team', id_team=id_team))

    player_data = Player.get_by_id(player_id)
    if not player_data:
        flash("Player does not exist.", "danger")
        return redirect(url_for('team.view_team', id_team=id_team))

    player = Player(**player_data)

    return render_template("players/view_player.html", player=player, id_team=id_team, team=team)

