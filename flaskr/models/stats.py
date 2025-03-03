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
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO t_stats (id_stat_type, id_player, id_match, value) VALUES (%s, %s, %s, %s)"
        , (self.id_stat_type, self.id_player, self.id_match, self.value))

        connection.commit()
        cursor.close()

    @staticmethod
    def get_stats_by_name(stat_name):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id FROM t_stats_type WHERE name = %s", (stat_name,)
        )
        stat = cursor.fetchone()
        cursor.close()

    @staticmethod
    def get_player_points(id_player):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COALESCE(SUM(value), 0) FROM t_stats WHERE id_player = %s AND id_stat_type IN (1, 2, 3)",
            (id_player,)
        )
        points = cursor.fetchone()  # Returns a tuple like (10,) or (None,)

        cursor.close()

        # Extract value from tuple and return as a dictionary
        return {'total_points': points[0] if points else 0}


