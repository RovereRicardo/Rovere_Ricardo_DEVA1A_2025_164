from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.WTForms.Forms import RegistrationForm, LoginForm
from flaskr.database.db import connection
from flaskr.models.user import User

user = Blueprint('user', __name__)

@user.route('/auth/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        role = form.role.data

        cursor = connection.cursor()
        cursor.execute("SELECT id_user FROM t_user WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            flash("Username already taken")
            return redirect(url_for('user.register'))

        hashed_password = password

        cursor = connection.cursor()
        cursor.execute("INSERT INTO t_user (username, name, email, password, role) VALUES (%s, %s, %s, %s, %s)",
                       (username, name, email, hashed_password, role))
        connection.commit()
        cursor.close()

        flash("Registration successful", "success")
        return redirect(url_for('user.login'))
    return render_template('auth/register.html', form=form)


@user.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        user = User.get_by_username(username)

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('user.login'))

    return render_template('auth/login.html', form=form)

@user.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))  # redirects to homepage