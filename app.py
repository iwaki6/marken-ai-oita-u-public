
# Initialize Flask application
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import flask_login

import os
import logging
import library.DBaccess as DBaccess
from library.model import User

APP_KEY = os.environ['MARKEN_APP_KEY'] # Set a secret word freely

# Initialize Flask application
app = Flask(__name__)
app.secret_key = APP_KEY

# Set up logging
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

# Configure LoginManager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
    
@login_manager.user_loader
def user_loader(email):
    user_info = DBaccess.inquire_user(email)
    if user_info is None:
        return
    
    user = User(user_info)
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    user_info = DBaccess.inquire_user(email)
    if user_info is None:
        return
    
    user = User(user_info)
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    # return 'Unauthorized', 401
    return redirect(url_for('app_login.login'))

# Load Modules
from app_login import module_login
app.register_blueprint(module_login)
from app_admin import module_admin
app.register_blueprint(module_admin)
from app_main import module_main
app.register_blueprint(module_main)


# Run the application if it is executed as the main script
if __name__ == '__main__':
    app.run(port=8080)
    #app.run()

