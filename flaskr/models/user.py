import pymysql
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from flaskr.database.db import connection

class User(UserMixin):
    def __init__(self, id_user, username, name, email, password, role):
        self.id_user = id_user
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    @staticmethod
    def get_by_username(username):
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM t_user WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return User(
                id_user=user_data['id_user'],
                username=user_data['username'],
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                role=user_data['role']
            )
        return None

    @staticmethod
    def get_by_id(user_id):
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM t_user WHERE id_user = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return User(
                id_user=user_data['id_user'],
                username=user_data['username'],
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                role=user_data['role']
            )
        return None

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id_user)
