from flask import render_template, session

from flaskr.database.db import connection

class Total:
    def __init__(self, id_match):
        self.id_match = id_match

    @staticmethod
    def get_total_points(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COALESCE(SUM(s.value), 0) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player = p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "JOIN t_match m ON s.id_match = m.id_match "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (1,2,3) "
            "AND tm.id_team = %s",
            (id_match, id_team)
        )

        result = cursor.fetchone()
        cursor.close()

        return result[0] if result and result[0] is not None else 0

    @staticmethod
    def get_total_lf_points(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(s.value), 0) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (1) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_lf_misses(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "

            "COALESCE(SUM(s.value), 0) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (9) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_lf(id_match, id_team):
        made = Total.get_total_lf_points(id_match, id_team)
        missed = Total.get_total_lf_misses(id_match, id_team)
        total_attempts = made[0]['total_points'] + missed[0]['total_points']
        return total_attempts

    @staticmethod
    def get_total_2pts(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(s.value), 0) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (2) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_2pts_made(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COUNT(s.value) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (2) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_2pts_misses(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COUNT(s.value) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (10) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_2pt_attempts(id_match, id_team):
        made = Total.get_total_2pts_made(id_match, id_team)
        missed = Total.get_total_2pts_misses(id_match, id_team)
        total_attempts = made[0]['total_points'] + missed[0]['total_points']
        return total_attempts


    @staticmethod
    def get_total_3pts_made(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COUNT(s.value) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (3) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_3pts_misses(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COUNT(s.value) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (11) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_3pt(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(s.value), 0) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (3) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_3pt_attempts(id_match, id_team):
        made = Total.get_total_3pts_made(id_match, id_team)
        missed = Total.get_total_3pts_misses(id_match, id_team)
        total = made[0]['total_points'] + missed[0]['total_points']
        return total

    @staticmethod
    def get_total_lf_percent(id_match, id_team):
        total = Total.get_total_lf(id_match, id_team)
        made = Total.get_total_lf_points(id_match, id_team)
        if total == 0:
            total_percent = 0
        else:
            total_percent = round((made[0]['total_points'] / total) * 100, 2)
        return total_percent

    @staticmethod
    def get_total_2pt_percent(id_match, id_team):
        made = Total.get_total_2pts_made(id_match, id_team)
        total = Total.get_total_2pt_attempts(id_match, id_team)
        if total == 0:
            total_percent = 0
        else:
            total_percent = round((made[0]['total_points'] / total) * 100, 2)
        return total_percent

    @staticmethod
    def get_total_3pt_percent(id_match, id_team):
        made = Total.get_total_3pts_made(id_match, id_team)
        total = Total.get_total_3pt_attempts(id_match, id_team)
        if total == 0:
            total_percent = 0
        else:
            total_percent = round((made[0]['total_points'] / total) * 100, 2)
        return total_percent

    @staticmethod
    def get_total_offensive_rebounds(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(s.value), 0) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (4) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_defensive_rebounds(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(s.value), 0) AS total_points "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (5) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_rebounds(id_match, id_team):
        offensive = Total.get_total_offensive_rebounds(id_match, id_team)
        defensive = Total.get_total_defensive_rebounds(id_match, id_team)
        total = offensive[0]['total_points'] + defensive[0]['total_points']
        return total

    @staticmethod
    def get_total_turnovers(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(s.value), 0) AS turnovers "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (6) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points

    @staticmethod
    def get_total_fouls(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT "
            "COALESCE(SUM(s.value), 0) AS fouls "
            "FROM t_stats s "
            "JOIN t_player p ON s.id_player =p.id_player "
            "JOIN t_team_player tp ON p.id_player = tp.id_player_team "
            "JOIN t_team tm ON tp.id_team_player = tm.id_team "
            "WHERE s.id_match = %s "
            "AND s.id_stat_type IN (7) "
            "AND (tm.id_team = %s)",
            (id_match, id_team)
        )
        points = cursor.fetchall()
        cursor.close()
        column_name = [desc[0] for desc in cursor.description]
        points = [dict(zip(column_name, row)) for row in points]
        return points