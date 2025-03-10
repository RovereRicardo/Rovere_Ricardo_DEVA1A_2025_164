from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.WTForms.RegistrationForm import RegistrationForm, LoginForm

from flaskr.database.db import connection
from flaskr.models.user import User

user = Blueprint('user', __name__)

@user.route('/auth/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        password = form.password.data
        password_hash = generate_password_hash(password)
        user = User(None, form.username.data, form.email.data, password_hash, form.role.data)
        user.register_user()

        flash("Registration successful")
        return redirect(url_for('index'))
    return render_template('/auth/register.html', form=form)

@user.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        cursor = connection.cursor()
        cursor.execute("SELECT username, id_user, password FROM t_user WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user is None or not check_password_hash(user[2], password): # Compare the password from form with password in db
            flash('Invalid username or password.', 'error')
            return redirect(url_for('user.login'))

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