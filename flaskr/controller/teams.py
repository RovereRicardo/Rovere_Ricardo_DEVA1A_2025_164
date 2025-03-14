from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from flaskr.WTForms.RegistrationForm import RegisterTeamForm, DeleteTeamForm, EditTeamForm
from flaskr.models.teams import Team  # Import the Team model
from flaskr.models.players import Player # Import Player model

team = Blueprint('team', __name__)

@team.route('/teams/register_team', methods=['GET', 'POST'])
def register_team():
    form = RegisterTeamForm(request.form)
    form.id_user.data = session.get('id_user')
    if request.method == 'POST' and form.validate():

        if not form.team_name.data:
            flash("Team Name is required.", "danger")
            return redirect(url_for('team.register_team'))

        new_team = Team(None, form.team_name.data, form.team_logo.data, form.address.data, form.city.data, form.wins.data, form.loses.data, form.draws.data, form.points.data, form.id_user.data) # Create team object
        new_team.register_team() # Call register function

        flash("Team Registered!", "success")
        return redirect(url_for('index'))
    return render_template('/teams/register_team.html', form=form)



@team.route('/teams/delete_team', methods=['POST'])
def delete_team():
    form = DeleteTeamForm(request.form)

    if not form.id_team.data:
        flash("Team does not exist.", "danger")
        return redirect(url_for('index'))

    try:
        team_data = Team.get_by_id(form.id_team.data)
        if not team_data:
            flash("Team does not exist.", "danger")
            return redirect(url_for('index'))

        team = Team(**team_data)

        if(team.id_coach_creator == session.get('id_user')):
            team.delete_team()
            flash("Team deleted!", "success")
        else:
            flash("You are not the coach of this team.", "danger")
    except Exception as e:
        flash(f"Error deleting team: {str(e)}", "danger")
    return redirect(url_for('index', form=form))

@team.route("/update/<int:id_team>", methods=["GET", "POST"])
def update_team(id_team):
    form = EditTeamForm(request.form)
    team_data = Team.get_by_id(id_team)
    if not team_data:
        flash("Team not found.", "danger")
        return redirect(url_for("index"))

    team = Team(**team_data)  # Create an instance of the Team class with the retrieved Data

    if request.method == 'GET':
        form.team_name.data = team.team_name
        form.team_logo.data = team.team_logo
        form.address.data = team.address
        form.city.data = team.city
        form.wins.data = team.wins
        form.loses.data = team.loses
        form.draws.data = team.draws
        form.points.data = team.points

    if request.method == "POST" and form.validate():
        team.team_name = form.team_name.data
        team.team_logo = form.team_logo.data
        team.address = form.address.data
        team.city = form.city.data
        team.wins = form.wins.data
        team.loses = form.loses.data
        team.draws = form.draws.data
        team.points = form.points.data

        team.update_team()  # Call the update_team method
        flash("Team Updated!", "success")
        return redirect(url_for("index"))

    return render_template("teams/update_team.html", team=team, form=form)

@team.route('/view_team/<int:id_team>', methods=('GET', 'POST'))
def view_team(id_team):
    team_data = Team.get_by_id(id_team)

    if not team_data:
        flash("Team not found.", "danger")
        return redirect(url_for('index'))

    team = Team(**team_data)

    player_data_list = Player.get_by_team(id_team)  # Returns a list of dictionaries

    players = [Player(**player_data) for player_data in player_data_list] # Create a list of players from player_data in player_data_list

    return render_template('/teams/view_team.html', team=team, username=session.get('username'), players=players)