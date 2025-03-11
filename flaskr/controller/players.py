
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from flaskr.WTForms.RegistrationForm import RegisterPlayerForm, EditPlayerForm, DeletePlayerForm
from flaskr.models.players import Player
from flaskr.models.teams import Team

player = Blueprint('player', __name__)

@player.route('/players/register_player', methods=['GET', 'POST'])
def register_player():
    form = RegisterPlayerForm(request.form)
    if request.method == 'POST' and form.validate():
        picture = form.picture.data

        id_team = request.args.get('id_team')

        if picture:
            picture_data = picture.read()  # Read the file content as binary data
        else:
            picture_data = None  # If no picture is uploaded, set to None

        if not form.name.data:
            flash('Player name is required.', 'danger')
            return redirect(url_for('player.register_player'))

        new_player = Player(form.name.data, form.family_name.data, picture_data, form.number.data, form.position.data, form.position_name.data, form.height.data, form.birthday.data, form.nationality.data)
        new_player.register_player(id_team)  # Call register function
        flash("Player registered successfully.", "success")

        return redirect(url_for('team.view_team', id_team=id_team, form=form))
    return render_template('/players/register_player.html' , id_team=request.args.get('id_team'), form=form)


@player.route('/delete_player', methods=['POST'])
def delete_player():
    form = DeletePlayerForm(request.form)

    if not form.id_player.data or not form.id_team.data:
        flash("Invalid player or team ID.", "danger")
        return redirect(url_for('index'))

    try:
        Player.delete_player(form.id_player.data, form.id_team.data)  # Call the delete function
        flash("Player deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting player: {str(e)}", "danger")

    return redirect(url_for('team.view_team', id_team=form.id_team.data, form=form))

@player.route('/update_player', methods=['POST', 'GET'])
def update_player():
    form = EditPlayerForm(request.form)
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
    if request.method == 'GET':
        form.name.data = player.name
        form.family_name.data = player.family_name
        form.number.data = player.number
        form.position.data = player.position
        form.position_name.data = player.position_name
        form.height.data = player.height
        form.birthday.data = player.birthday
        form.nationality.data = player.nationality

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

    return render_template("players/update_player.html", username= session.get('username'), player=player, team=team, form=form)

@player.route('/view_player', methods=['GET', 'POST'])
def view_player():
    player_id = request.args.get('player_id', type=int)
    id_team = request.args.get('id_team', type=int)

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

    return render_template("players/view_player.html", username=session.get('username'), player=player, id_team=id_team, team=team)

