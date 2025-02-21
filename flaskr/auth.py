import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.db import connection

auth = Blueprint('auth', __name__)


# User Registration
@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        confirmPassword = request.form['confirm_password']

        if not username or not password:
            flash('Username and password are required!', 'error')
            return redirect(url_for('auth.register'))

        cursor = connection.cursor()
        cursor.execute("SELECT id_user FROM t_user WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already taken.', 'error')
            return redirect(url_for('auth.register'))

        if password != confirmPassword:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))

        password = generate_password_hash(password)
        cursor.execute("INSERT INTO t_user (username, email, password, role) VALUES (%s, %s,%s, %s)",
                       (username, email, password, role))
        connection.commit()
        cursor.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('/auth/register.html')


# User Login
@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = connection.cursor()
        cursor.execute("SELECT username, id_user, password FROM t_user WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user is None or not check_password_hash(user[2], password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))

        session.permanent = True  # Ensures session lasts as configured
        session['username'] = user[0]
        session['id_user'] = user[1]
        flash('Login successful!', 'success')
        return redirect(url_for('index'))

    return render_template('/auth/login.html')



# User Logout
@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()  # Clears the user session
    return redirect(url_for("index"))  # Redirects to homepage


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'id_user' not in session:  # Use 'id_user' instead of 'user_id'
            flash("You need to log in first.", "error")
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapped_view

