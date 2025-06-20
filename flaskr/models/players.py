import pymysql

from flaskr.database.db import connection


class Player:
    def __init__(self, name=None, family_name=None, picture=None, number=None, position=None, position_name=None, height=None, birthday=None, nationality=None,
                 id_player=None, is_deleted=None, id_team=None):
        self.id_player = id_player
        self.name = name
        self.family_name = family_name
        self.number = number
        self.picture = picture
        self.position = position
        self.position_name = position_name
        self.height = height
        self.birthday = birthday
        self.nationality = nationality
        self.is_deleted = is_deleted
        self.id_team = id_team

    @staticmethod
    def get_by_team(id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT p.* FROM t_player p JOIN t_team_player tp ON p.id_player = tp.id_player_team JOIN t_team t ON tp.id_team_player = t.id_team WHERE t.id_team = %s",
            (id_team,))
        players = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        players = [dict(zip(column_names, player)) for player in players]

        return players

    def register_player(self, id_team):
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO t_player(name, family_name, picture, number, position, position_name, height, birthday, nationality) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)",
            (self.name, self.family_name, self.picture, self.number, self.position, self.position_name, self.height, self.birthday,
             self.nationality)
        )

        id_player = cursor.lastrowid
        connection.commit()

        cursor.execute(
            "INSERT INTO t_team_player (id_team_player, id_player_team) VALUES (%s, %s)",
            (id_team, id_player)
        )
        connection.commit()

        cursor.close()

    @staticmethod
    def get_match_players(id_team, id_match):
        cursor = connection.cursor()
        cursor.execute("SELECT pm.id_match, tm.id_team AS team_id, tm.team_name, p.id_player, p.name, p.family_name, pm.subbed, pm.played FROM t_players_match pm JOIN t_player p ON pm.id_player = p.id_player JOIN t_team_player tp ON p.id_player = tp.id_player_team JOIN t_team tm on tp.id_team_player = tm.id_team JOIN t_match m ON pm.id_match = m.id_match WHERE m.id_match = %s AND tm.id_team = %s AND pm.played = 1",
                       (id_match, id_team,))
        players = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        players = [dict(zip(column_names, player)) for player in players]
        return players

    def delete_player(id_player, id_team):
        cursor = connection.cursor()

        cursor.execute("UPDATE t_player SET is_deleted = 1 WHERE id_player = %s", (id_player,))

        connection.commit()
        cursor.close()

    def update_player(self):
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE t_player SET name=%s, family_name=%s, picture=%s, number=%s, position=%s, position_name=%s, height=%s, birthday=%s, nationality=%s, is_deleted=0 WHERE id_player = %s",
            (self.name, self.family_name, self.picture, self.number, self.position, self.position_name, self.height, self.birthday,self.nationality, self.id_player)
        )
        connection.commit()
        cursor.close()

    @staticmethod
    def get_by_id(id_player):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM t_player WHERE id_player = %s", (id_player,)
        )
        player = cursor.fetchone()

        column_names = [desc[0] for desc in cursor.description]
        player_dict = dict(zip(column_names, player))
        cursor.close()
        return Player(**player_dict)

    @staticmethod
    def get_all_players(self):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT p.*, t.id_team FROM t_player p JOIN t_team_player tp ON p.id_player = tp.id_player_team JOIN t_team t ON tp.id_team_player = t.id_team",
        )
        players = cursor.fetchall()
        cursor.close()
        column_names = [desc[0] for desc in cursor.description]
        players = [dict(zip(column_names, player)) for player in players]

        return players