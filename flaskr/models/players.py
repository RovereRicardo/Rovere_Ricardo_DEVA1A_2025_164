from flaskr.database.db import connection


class Player:
    def __init__(self, name, family_name, picture, number, position, position_name, height, birthday, nationality,
                 id_player=None, is_deleted=None):
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

    @staticmethod
    def get_by_team(id_team):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT p.* FROM t_player p JOIN t_team_player tp ON p.id_player = tp.id_player_team JOIN t_team t ON tp.id_team_player = t.id_team WHERE t.id_team = %s AND p.is_deleted = 0",
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

    def delete_player(id_player, id_team):
        cursor = connection.cursor()

        # Delete from the association table
        """cursor.execute("DELETE FROM t_team_player WHERE id_player_team = %s AND id_team_player = %s",
                       (id_player, id_team))

        # Check if the player is still linked to another team
        cursor.execute("SELECT COUNT(*) FROM t_team_player WHERE id_player_team = %s", (id_player,))
        count = cursor.fetchone()[0]

        if count == 0:  # If player is not in any other team, delete from players table
            cursor.execute("DELETE FROM t_player WHERE id_player = %s", (id_player,))"""

        cursor.execute("UPDATE t_player SET is_deleted = 1 WHERE id_player = %s", (id_player,))

        connection.commit()
        cursor.close()

    def update_player(self):
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE t_player SET name=%s, family_name=%s, number=%s, position=%s, position_name=%s, height=%s, birthday=%s, nationality=%s WHERE id_player = %s",
            (self.name, self.family_name, self.number, self.position, self.position_name, self.height, self.birthday,self.nationality, self.id_player)
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
        player = dict(zip(column_names, player))
        cursor.close()
        return player
