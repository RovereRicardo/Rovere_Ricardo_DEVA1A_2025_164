from flaskr.database.db import connection

class Matchs:
    def __init__(self,id_match, date_match, id_home_team, id_away_team, home_score = None, away_score = None, home_team = None, away_team = None):
        self.id_match = id_match
        self.date_match = date_match
        self.id_home_team = id_home_team
        self.id_away_team = id_away_team
        self.home_score = home_score
        self.away_score = away_score
        self.home_team = home_team
        self.away_team = away_team

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