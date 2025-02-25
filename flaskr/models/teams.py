from flask import render_template, session
from flaskr.models.db import connection

class Team:
    def __init__(self, id_team, team_name, team_logo, address, city, wins, loses, draws, points, id_coach_creator):
        self.id_team = id_team
        self.team_name = team_name
        self.team_logo = team_logo
        self.address = address
        self.city = city
        self.wins = wins
        self.loses = loses
        self.draws = draws
        self.points = points
        self.id_coach_creator = id_coach_creator

    def register_team(self):
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO t_team (team_name, team_logo, address, city, wins, loses, draws, points, id_coach_creator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (self.team_name, self.team_logo, self.address, self.city, self.wins, self.loses, self.draws, self.points, self.id_coach_creator))
        connection.commit()
        cursor.close()

    def delete_team(self):
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM t_team WHERE id_team = %s",
            (self.id_team,)  # Ensure it's a tuple
        )
        connection.commit()
        cursor.close()

    def update_team(self):
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE t_team SET team_name=%s, team_logo=%s, address=%s, city=%s, wins=%s, loses=%s, draws=%s, points=%s WHERE id_team=%s",
            (self.team_name, self.team_logo, self.address, self.city, self.wins, self.loses, self.draws, self.points, self.id_team))
        connection.commit()
        cursor.close()

    def view_team(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM t_team WHERE id_team = %s", (self.team_id,))
        team = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]
        team = dict(zip(column_names, team))

        cursor.execute(
            "SELECT p.* FROM t_player p JOIN t_team_player tp ON p.id_player = tp.id_player_team JOIN t_team t ON tp.id_team_player = t.id_team WHERE t.id_team = %s",
            (self.team_id,))
        players = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        players = [dict(zip(column_names, player)) for player in players]

        return render_template("/teams/view_team.html", team=team, username=session.get('username'), players=players)

    @staticmethod
    def get_by_id(team_id):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM t_team WHERE id_team = %s", (team_id,))
        team = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]
        team = dict(zip(column_names, team))
        cursor.close()

        return team