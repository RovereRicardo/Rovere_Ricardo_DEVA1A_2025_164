from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user

from flaskr.WTForms.Forms import TeamForm, DeleteTeamForm
from flaskr.models.teams import Team  # Import the Team model
from flaskr.models.players import Player # Import Player model
from flaskr.models.user import User

team = Blueprint('team', __name__)

@team.route('/teams/team', defaults={'id_team':None}, methods=['GET', 'POST'])
@team.route('/teams/team/<int:id_team>', methods=['GET', 'POST'])
@login_required
def register_team(id_team):
    form = TeamForm()
    form.id_user.data = current_user.get_id()

    team = Team.get_by_id(id_team) if id_team else Team()

    print(team)
    if request.method == 'GET':
        if id_team:
            form = TeamForm(**vars(team))

    if form.validate_on_submit():
        picture = request.files['team_logo']
        picture_data = picture.read() if picture else None

        for field in form._fields.keys():
            setattr(team, field, getattr(form, field).data)

        setattr(team, 'id_team', id_team)
        setattr(team, 'id_coach_creator', current_user.get_id())
        setattr(team, 'team_logo', picture_data)

        if id_team:
            team.update_team()
            flash("Team updated successfully.", "success")
        else:
            team.register_team()
            flash('Team registered successfully.', 'success')

        return redirect(url_for('team.view_teams'))

    # Display form validation errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", "danger")

    return render_template('/teams/register_team.html', form=form, team=team)

@team.route('/teams/delete_team', methods=['POST'])
@login_required
def delete_team():
    form = DeleteTeamForm(request.form)

    if not form.id_team.data:
        flash("Team does not exist.", "danger")
        return redirect(url_for('index'))

    try:
        team = Team.get_by_id(form.id_team.data)
        if not team:
            flash("Team does not exist.", "danger")
            return redirect(url_for('team.view_teams'))

        team = Team(**vars(team))
        print(current_user.get_id())
        print(team.id_coach_creator)
        if int(team.id_coach_creator) == int(current_user.get_id()):
            team.delete_team()
            flash("Team deleted!", "success")
        else:
            flash("You are not the coach of this team.", "danger")
    except Exception as e:
        flash(f"Error deleting team: {str(e)}", "danger")
    return redirect(url_for('team.view_teams', form=form))

@team.route('/view_team/<int:id_team>', methods=('GET', 'POST'))
def view_team(id_team):
    team_data = Team.get_by_id(id_team)

    if not team_data:
        flash("Team not found.", "danger")
        return redirect(url_for('index'))

    team = Team(**vars(team_data))

    player_data_list = Player.get_by_team(id_team)  # Returns a list of dictionaries

    players = [Player(**player_data) for player_data in player_data_list] # Create a list of players from player_data in player_data_list


    return render_template('/teams/view_team.html', team=team, players=players, id_team=id_team, username=session.get('id_user'))

@team.route('/teams', methods=('GET', 'POST'))
def view_teams():
    teams = Team.get_all_teams()

    return render_template('/teams/teams.html', teams=teams)

@team.route('/ranking', methods=('GET', 'POST'))
def ranking():
    teams = Team.get_all_teams()
    return render_template('/teams/ranking.html', teams=teams, position=1)

@team.route('/team_details/<int:id_team>', methods=('GET', 'POST'))
def team_details(id_team):
    team_data = Team.get_by_id(id_team)

    if not team_data:
        flash("Team not found.", "danger")
        return redirect(url_for('index'))

    team = Team(**vars(team_data))

    coach = Team.get_coach(team)

    return render_template('/teams/team_details.html', id_team=id_team, team=team, coach=coach)