from flask import Blueprint, request, redirect, url_for
from flaskr.models.stats import Stats

stat = Blueprint('stat', __name__)


@stat.route('/register_stat', methods=['POST'])
def register_stat():
    id_player = request.form.get('idPlayer')
    id_match = request.form.get('idMatch')
    stat_type = request.form.get('statType')
    stat_value = request.form.get('statValue')

    stat_type_id = Stats.get_stats_by_name(stat_type)

    if stat_type_id:
        # Create a Stats instance and register it
        new_stat = Stats(stat_type_id, id_player, id_match, stat_value)
        new_stat.register_stat()
        return redirect(url_for('match.view_match', id_match=id_match))
    else:
        return "Error: Stat type not found", 400