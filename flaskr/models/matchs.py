from logging import exception
from warnings import catch_warnings

from click import confirm
from flask import flash

from flaskr.database.db import connection


class Matchs:
    def __init__(self, id_match, date_match, id_home_team, id_away_team, home_score=None, away_score=None,
                 home_team=None, away_team=None):
        self.id_match = id_match
        self.date_match = date_match
        self.id_home_team = id_home_team
        self.id_away_team = id_away_team
        self.home_score = home_score
        self.away_score = away_score
        self.home_team = home_team
        self.away_team = away_team

    @staticmethod
    def get_match_by_id(id_match):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT m.id_match, m.id_home_team, m.id_away_team, home_team.team_name AS home_team, away_team.team_name AS away_team, m.date_match, m.home_score, m.away_score FROM t_match m JOIN t_team home_team ON m.id_home_team = home_team.id_team JOIN t_team away_team ON m.id_away_team = away_team.id_team WHERE id_match = %s",
            (id_match,))
        match = cursor.fetchone()

        column_names = [desc[0] for desc in cursor.description]
        match = dict(zip(column_names, match))
        cursor.close()
        return match

    @staticmethod
    def get_by_id(id_match):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM t_match WHERE id_match = %s", (id_match,))
        match = cursor.fetchone()

        column_names = [desc[0] for desc in cursor.description]
        match = dict(zip(column_names, match))
        cursor.close()
        return match

    def register_match(self):
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO t_match (date_match, id_home_team,id_away_team) VALUES (%s,%s,%s)",
            (self.date_match, self.id_home_team, self.id_away_team)
        )
        connection.commit()
        cursor.close()

    def delete_match(self):
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM t_match WHERE id_match = %s",
            (self.id_match)
        )

        connection.commit()
        cursor.close()

    def edit_match(self):
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE t_match SET date_match = %s, id_home_team = %s, id_away_team = %s, home_score = %s, away_score = %s WHERE id_match=%s",
            (self.date_match, self.id_home_team, self.id_away_team, self.home_score, self.away_score, self.id_match))
        connection.commit()
        connection.close()

    @staticmethod
    def add_player_to_mach(id_match, id_player):
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO t_players_match (id_match, id_player) VALUES (%s, %s)", (id_match, id_player)
            )
            connection.commit()
            cursor.close()
            flash("Player added successfully!", "success")
        except Exception as e:  # Catch the exact error
            print("Error adding player to match:", e)  # Debugging output
            flash(f"Error: {str(e)}", "danger")  # Show the actual error in the UI

    @staticmethod
    def get_players_playing(id_match, id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT pm.id_match, tm.id_team AS team_id, tm.team_name, p.id_player, p.name, p.family_name FROM t_players_match pm JOIN t_player p ON pm.id_player = p.id_player JOIN t_team_player tp ON p.id_player = tp.id_player_team JOIN t_team tm on tp.id_team_player = tm.id_team JOIN t_match m ON pm.id_match = m.id_match WHERE m.id_match = %s AND tm.id_team = %s",
            (id_match, id_team)
        )
        players = cursor.fetchall()
        column_name = [desc[0] for desc in cursor.description]
        players = [dict(zip(column_name, row)) for row in players]
        cursor.close()

        return players

    @staticmethod
    def submit_score(id_match,home_score,away_score):
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE t_match SET home_score = %s, away_score = %s WHERE id_match = %s",
            (home_score, away_score, id_match)
        )
        connection.commit()
        cursor.close()

    @staticmethod
    def set_win(id_team):
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE t_team SET wins = wins + 1 WHERE id_team = %s",
            (id_team,)
        )
        connection.commit()
        cursor.close()

    @staticmethod
    def set_lose(id_team):
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE t_team SET loses = loses + 1 WHERE id_team = %s",
            (id_team,)
        )
        connection.commit()
        cursor.close()
