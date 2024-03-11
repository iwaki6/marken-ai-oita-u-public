from flask import Blueprint, request, redirect, url_for, render_template
import flask_login

import library.DBaccess as DBaccess
import library.password
from library.model import User

module_login = Blueprint('app_login', __name__, url_prefix='')

@module_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_form.html')

    email = request.form['email']
    user_info = DBaccess.inquire_user(email)
    if user_info is None:
        return 'Bad login'
    if library.password.check_password(request.form['password'], user_info):
        user = User(user_info)
        flask_login.login_user(user)
        if user.role == 'admin':
            return redirect(url_for('app_admin.admin_world'))
        return redirect(url_for('app_login.protected'))

    return 'Bad login'

@module_login.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@module_login.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'
