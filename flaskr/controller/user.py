from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.database.db import connection
from flaskr.models.user import User

user = Blueprint('user', __name__)

@user.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('user.register'))


        password = generate_password_hash(password)
        user = User(None, username, email, password, role)
        user.register_user()

        return redirect(url_for('index'))
    return render_template('/auth/register.html')

@user.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = connection.cursor()
        cursor.execute("SELECT username, id_user, password FROM t_user WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user is None or not check_password_hash(user[2], password): # Compare the password from form with password in db
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))

        session.permanent = True  # Permanent session
        session['username'] = user[0]
        session['id_user'] = user[1]
        flash('Login successful!', 'success')
        return redirect(url_for('index'))

    return render_template('/auth/login.html')

@user.route("/logout", methods=["POST"])
def logout():
    session.clear()  # Clears the user session
    return redirect(url_for("index"))  # Redirects to homepage