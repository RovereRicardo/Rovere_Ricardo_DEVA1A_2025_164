from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flaskr.models.teams import Team  # Import the Team model
from flaskr.models.players import Player # Import Player model

team = Blueprint('team', __name__)

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

        new_team = Team(None, team_name, team_logo, address, city, wins, loses, draws, points, id_user) # Create team object
        new_team.register_team() # Call register function

        flash("Team Registered!", "success")
        return redirect(url_for('index'))
    return render_template('/teams/register_team.html')

@team.route('/teams/delete_team', methods=['POST'])
def delete_team():
    if request.method == 'POST':
        team_id = request.form['id_team']

        team_data = Team.get_by_id(team_id)

        if not team_data:
            flash("Team does not exist.", "danger")
            return redirect(url_for('index'))

        team = Team(**team_data)
        team.delete_team()

        flash("Team Deleted!", "success")
        return redirect(url_for('index'))

@team.route("/update/<int:team_id>", methods=["GET", "POST"])
def update_team(team_id):
    team_data = Team.get_by_id(team_id)
    if not team_data:
        flash("Team not found.", "danger")
        return redirect(url_for("index"))

    team = Team(**team_data)  # Create an instance of the Team class with the retrieved Data

    if request.method == "POST":
        team.team_name = request.form["team_name"]
        team.team_logo = request.form["team_logo"]
        team.address = request.form["address"]
        team.city = request.form["city"]
        team.wins = request.form["wins"]
        team.loses = request.form["loses"]
        team.draws = request.form["draws"]
        team.points = request.form["points"]

        team.update_team()  # Call the update_team method
        flash("Team Updated!", "success")
        return redirect(url_for("index"))

    return render_template("teams/update_team.html", team=team)

@team.route('/view_team/<int:team_id>', methods=('GET', 'POST'))
def view_team(team_id):
    team_data = Team.get_by_id(team_id)

    if not team_data:
        flash("Team not found.", "danger")
        return redirect(url_for('index'))

    team = Team(**team_data)

    player_data_list = Player.get_by_team(team_id)  # Returns a list of dictionaries

    players = [Player(**player_data) for player_data in player_data_list] # Create a list of players from player_data in player_data_list

    return render_template('/teams/view_team.html', team=team, username=session.get('username'), players=players)