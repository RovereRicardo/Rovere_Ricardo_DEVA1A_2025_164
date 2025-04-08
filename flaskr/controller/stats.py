from bokeh.embed import components
from bokeh.plotting import figure
from flask import Blueprint, request, redirect, url_for, render_template, session

from flaskr.models.players import Player
from flaskr.models.stats import Stats
from flaskr.models.matchs import Matchs
from flaskr.models.teams import Team

stat = Blueprint('stat', __name__)


@stat.route('/register_stat', methods=['POST'])
def register_stat():
    id_player = request.form.get('idPlayer')
    id_match = request.form.get('idMatch')
    stat_type = request.form.get('statType')
    stat_value = request.form.get('statValue')

    stat_type_id = Stats.get_stats_by_name(stat_type)

    if stat_type_id:
        # creation de la stat et la registre
        new_stat = Stats(stat_type_id, id_player, id_match, stat_value)
        new_stat.register_stat()
        return redirect(url_for('match.view_match', id_match=id_match))
    else:
        return "Error: Stat type not found", 400

@stat.route('/player_stats/<int:id_player>/team/<int:id_team>', methods=['GET','POST'])
def player_stats(id_player, id_team):

    matches = Matchs.get_all_matches()
    player = Player.get_by_id(id_player)
    team = Team.get_by_id(id_team)

    x = [str(match['id_match']) for match in matches] # Axis de x
    y = [int(Stats.get_player_graph(id_player, match['id_match'])['count']) for match in matches] #Axis de y = Total per match


    p = figure(x_range=x, height=600,width=1440, toolbar_location=None, tools="")
    p.vbar(x=x,top=y, width=0.5)
    p.y_range.start = 0
    p.ygrid.visible = False

    script, div = components(p)

    print("Matches:", matches)  # Debugging
    for match in matches:
        count = Stats.get_player_graph(id_player, match['id_match'])['count']
        print(f"Match ID: {match['id_match']}, Count: {count}")

    return render_template("players/view_player.html",team=team ,player=player, script=script, div=div, id_team=id_team,id_player=id_player)

