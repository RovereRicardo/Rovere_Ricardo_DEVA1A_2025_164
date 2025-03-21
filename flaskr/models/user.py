from flask import redirect, url_for, flash
from flaskr.database.db import connection

class User:
    def __init__(self, id_user, username, name, email, password, role):
        self.id_user = id_user
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def register_user(self):

        cursor = connection.cursor()
        cursor.execute("SELECT id_user FROM t_user WHERE username = %s", (self.username,))
        exists = cursor.fetchone()

        if exists:
            flash('Username already taken', 'error')
            return redirect(url_for('user.register'))

        cursor.execute("INSERT INTO t_user (username, name, email, password, role) VALUES (%s, %s, %s, %s, %s)",
                       (self.username, self.name, self.email, self.password, self.role))

        user_id = cursor.lastrowid
        connection.commit()

        cursor.execute("INSERT INTO t_coach(id_user) VALUES (%s)", (user_id))
        connection.commit()
        cursor.close()

    @staticmethod
    def get_coach(id_user):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM t_user WHERE id_user = %s",(id_user,))
        user = cursor.fetchone()

        return user
