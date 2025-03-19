from flask import render_template, session

from flaskr.database import db
from flaskr.database.db import connection

class Stats:
    def __init__(self, id_stat_type, id_player, id_match, value):
        self.id_stat_type = id_stat_type
        self.id_player = id_player
        self.id_match = id_match
        self.value = value

    def register_stat(self):
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO t_stats (id_stat_type, id_player, id_match, value) VALUES (%s, %s, %s, %s)"
            , (self.id_stat_type, self.id_player, self.id_match, self.value))

            connection.commit()
        except Exception as e:
            print(f"Error entering stat: {e}")
        finally:
            cursor.close()

    @staticmethod
    def get_stats_by_name(stat_name):
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id FROM t_stats_type WHERE name = %s", (stat_name,)
            )
            stat = cursor.fetchone()
            return stat[0] if stat else None
        except Exception as e:
            print(f"Error entering stat: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_player_points(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (1, 2, 3)",
            (id_player,id_match)
        )
        points = cursor.fetchone()  # Returns a tuple like (10,) or (None,)

        cursor.close()

        # Extract value from tuple and return as a dictionary
        return {'total_points': points[0] if points else 0}

    @staticmethod
    def get_player_lf(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) AS total_LFMade FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (1)",
            (id_player, id_match))
        points = cursor.fetchone()
        cursor.close()
        return {'total_LFMade': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_lf_miss(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) AS total_LFMiss FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (9)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_LFMiss': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_total_lf(id_player, id_match):
        made = Stats.get_player_lf(id_player, id_match)
        missed = Stats.get_player_lf_miss(id_player, id_match)

        total_made = made['total_LFMade'] + missed['total_LFMiss']
        return total_made

    @staticmethod
    def get_player_lf_percent(id_player, id_match):
        made = Stats.get_player_lf(id_player, id_match)
        total_lf = Stats.get_player_total_lf(id_player, id_match)
        if total_lf == 0:
            return 0
        else:
            total_percent = round((made['total_LFMade'] / total_lf) * 100, 2)
        return total_percent

    @staticmethod
    def get_player_2pt(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) as total_2PT FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (2)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_2pt': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_2pt_miss(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(value) as total_2PT_Miss FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (10)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_2pt_miss': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_2pt_made(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(value) as total_2pt_made FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (2)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_2pt_made': points[0] if points and points[0] is not None else 0}


    @staticmethod
    def get_player_2pt_total(id_player, id_match):
        made = Stats.get_player_2pt_made(id_player, id_match)
        missed = Stats.get_player_2pt_miss(id_player, id_match)
        total_made = made['total_2pt_made'] + missed['total_2pt_miss']
        return total_made

    @staticmethod
    def get_player_2pt_percent(id_player, id_match):
        made = Stats.get_player_2pt_made(id_player, id_match)
        total_2pt = Stats.get_player_2pt_total(id_player, id_match)
        if total_2pt == 0:
            return 0
        else:
            total_percent = round((made['total_2pt_made'] / total_2pt) * 100, 2)
        return total_percent

    @staticmethod
    def get_player_3pt(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) as total_3PT FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (3)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_3pt': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_3pt_miss(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(value) as total_3PT_Miss FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (11)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_3PT_Miss': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_3pt_made(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(value) as total_3pt_made FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (3)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_3pt_made': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_3pt_total(id_player, id_match):
        made = Stats.get_player_3pt_made(id_player, id_match)
        missed = Stats.get_player_3pt_miss(id_player, id_match)
        total_made = made['total_3pt_made'] + missed['total_3PT_Miss']
        return total_made

    @staticmethod
    def get_player_3pt_percent(id_player, id_match):
        made = Stats.get_player_3pt_made(id_player, id_match)
        total_3pt = Stats.get_player_3pt_total(id_player, id_match)
        if total_3pt == 0:
            return 0
        else:
            total_percent = round((made['total_3pt_made'] / total_3pt) * 100, 2)
        return total_percent

    @staticmethod
    def get_player_offensive_rebounds(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) as total_rebs FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (4)",
            (id_player,id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_offensive': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_defensive_rebounds(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) as total_rebs FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (5)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_defensive': points[0] if points and points[0] is not None else 0}


    @staticmethod
    def get_player_total_rebounds(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) as total_rebs FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (4,5)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'total_rebs': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_turnovers(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) as total_rebs FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (6)",
            (id_player,id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'turnovers': points[0] if points and points[0] is not None else 0}

    @staticmethod
    def get_player_fouls(id_player, id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT SUM(value) as total_rebs FROM t_stats WHERE id_player = %s AND id_match = %s AND id_stat_type IN (7)",
            (id_player, id_match)
        )
        points = cursor.fetchone()
        cursor.close()
        return {'fouls': points[0] if points and points[0] is not None else 0}
