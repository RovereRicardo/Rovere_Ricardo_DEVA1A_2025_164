
from bokeh.plotting import figure
from dominate.tags import script
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, jsonify
from bokeh.embed import components
from flask_login import login_required

from flaskr.WTForms.Forms import PlayerForm, DeletePlayerForm
from flaskr.models.matchs import Matchs
from flaskr.models.players import Player
from flaskr.models.stats import Stats
from flaskr.models.teams import Team
from bokeh.models.sources import AjaxDataSource
from flaskr.database.db import connection

player = Blueprint('player', __name__)

@player.route('/players/player', defaults={'id_player': None}, methods=['GET', 'POST'])
@player.route('/players/player/<int:id_player>', methods=['GET', 'POST'])
@login_required
def register_player(id_player):
    form = PlayerForm()
    id_team = request.args.get('id_team', type=int)  # Get the team ID from the query string

    # Get the existing player or create a new one
    player = Player.get_by_id(id_player) if id_player else Player()

    if request.method == 'GET':
        # Fill form with existing data if the player exists
        if id_player:
            form = PlayerForm(**vars(player))  # Fill the form with existing data

    if form.validate_on_submit():
        picture = request.files['picture']
        picture_data = picture.read() if picture else None

        for field in form._fields.keys():
            setattr(player, field, getattr(form, field).data)

        setattr(player, 'picture', picture_data)
        setattr(player, 'id_team', id_team)

        if id_player:
            player.update_player()
            flash("Player updated successfully.", "success")
        else:
            player.register_player(id_team)
            flash("Player registered successfully.", "success")

        return redirect(url_for('team.view_team', id_team=id_team))

    return render_template('players/register_player.html', form=form, player=player, id_team=id_team)

@player.route('/delete_player', methods=['POST'])
@login_required
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

@player.route('/view_player/<int:id_player>/team/<int:id_team>', methods=['GET', 'POST'])
def view_player(id_player, id_team):
    stat_type = request.args.get('stat_type', default=1)
    team = None

    if id_team:
        team_data = Team.get_by_id(id_team)
        if team_data:
            team = Team(**vars(team_data))  # Convert data to Team object

    if not id_player:
        flash("Player ID is missing.", "danger")
        return redirect(url_for('team.view_team', id_team=id_team))

    player_data = Player.get_by_id(id_player)
    if not player_data:
        flash("Player does not exist.", "danger")
        return redirect(url_for('team.view_team', id_team=id_team))

    player = Player(**vars(player_data))

    script_lf, div_lf = generate_plot(id_player, 1)
    script_2pt, div_2pt = generate_plot(id_player, 2)
    script_3pt, div_3pt = generate_plot(id_player, 3)
    script_points, div_points = generate_plot_points(id_player)

    return render_template("players/view_player.html",script_points=script_points, div_points=div_points, script_lf=script_lf, div_lf=div_lf, script_2pt=script_2pt, div_2pt=div_2pt, script_3pt=script_3pt, div_3pt=div_3pt, username=session.get('username'), player=player, id_team=id_team, team=team)

@player.route('/players', methods=['GET', 'POST'])
def view_all_players():
    players = Player.get_all_players(Player)

    return render_template('/players/players.html', players=players, username=session.get('username'))

"""
@player.route('/view_player_ajax', methods=['GET', 'POST'])
def view_player_ajax():
    id_player = request.args.get('id_player')
    stat_type = request.args.get('stat_type')

    print(f"Request Arguments: id_player={id_player}, stat_type={stat_type}")

    # Fetch all matches and the stat for the player
    matches = Matchs.get_all_matches()

    x = [str(match['id_match']) for match in matches]
    y = [
        int(Stats.get_player_graph(id_player, match['id_match'], stat_type).get('count', 0))
        for match in matches
    ]

    # Log the data to check the response
    print(f"x: {x}")
    print(f"y: {y}")

    # Generate the Bokeh graph
    p = figure(x_range=x, height=600, width=1440, toolbar_location=None, tools="")
    p.vbar(x=x, top=y, width=0.5)
    p.y_range.start = 0
    p.ygrid.visible = False

    script, div = components(p)

    print(f"Generated Div: {div}")
    print(f"Generated Script: {script}")

    return div + script
    """

def generate_plot(id_player, stat_type):
    matches = Matchs.get_all_matches()

    # Get match IDs and corresponding stats
    x = [str(match['id_match']) for match in matches]
    y = [
        int(Stats.get_player_graph(id_player, match['id_match'], stat_type).get('count', 0))
        for match in matches
    ]
    if(stat_type == 1):
        title = "LF Per Game"
    elif(stat_type == 2):
        title = "2PT Per Game"
    elif(stat_type == 3):
        title = "3PT Per Game"

    # Create the Bokeh plot
    p = figure(x_range=x, height=600, width=1440 ,title=title)
    p.line(x,y, line_width=0.5)
    p.scatter(x,y,fill_color="red",size=15)
    p.xaxis.axis_label = 'Match ID'
    p.yaxis.axis_label = title
    p.y_range.start = 0
    p.ygrid.visible = False

    # Generate the script and div for embedding
    script, div = components(p)

    return script, div

def generate_plot_points(id_player):
    matches = Matchs.get_all_matches()
    x = [str(match['id_match']) for match in matches]
    y = [int(Stats.get_player_graph_total(id_player,match['id_match']).get('count', 0)) for match in matches]

    p = figure(x_range=x, height=600, width=1440, title="Points per Game")
    p.line(x,y, width=0.5)
    p.scatter(x,y,fill_color="red", size=15)
    p.xaxis.axis_label = 'Match ID'
    p.yaxis.axis_label = "Points per Game"
    p.y_range.start = 0
    p.ygrid.visible = False
    script, div = components(p)
    return script, div