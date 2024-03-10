from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response
import flask_login

import os
import datetime
from library.model import CodeEntries
import library.DBaccess as DBaccess

module_admin = Blueprint('app_admin', __name__, url_prefix='/admin_world')

pM = CodeEntries()

# Management Screen for SuperUser

@module_admin.route('/')
@flask_login.login_required
def admin_world():
    if flask_login.current_user.role == 'admin':
        return render_template('index_admin.html')
    return redirect(url_for('index'))

@module_admin.route('/export', methods=['POST'])
@flask_login.login_required
def export():
    data = request.get_json()
    passcode = str(data.get('passcode'))
    user = flask_login.current_user
    if user.role == 'admin':
        registered = pM.get(user.id)
        if registered.passcode is None:
            return jsonify({
                'text': "Issue a new passcode and use it.", 
                'success': False
            })
        if registered.timeLimit < datetime.datetime.now():
            return jsonify({
                'text': "Issue a new passcode and use it.",
                'success': False
            })
        if registered.passcode != passcode:
            return jsonify({
                'text': "Incorrect passcode.",
                'success': False
            })
        if not DBaccess.export():
            return jsonify({
                'text': "Data base error.",
                'success': False
            })

        pM.remove(user.id)
        return jsonify({
            'text': "Now, the file is downloaded.",
            'success': True
        })
    return "You don't have the authority to access."

@module_admin.route('/download')
@flask_login.login_required
def download():
    user = flask_login.current_user
    if user.role == 'admin':
        with open(DBaccess.FILEPATH, "rb") as f:
            data = f.read()
            f.close()
        os.remove(DBaccess.FILEPATH)
        output = make_response()
        output.data = data
        output.headers["Content-Disposition"] = "attachment; filename=result.xlsx"
        output.mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return output
    
    return "You don't have the authority to access."

@module_admin.route('/clearDB', methods=['POST'])
@flask_login.login_required
def clearDB():
    data = request.get_json()
    passcode = str(data.get('passcode'))
    user = flask_login.current_user
    if user.role == 'admin':
        registered = pM.get(user.id)
        if registered.passcode is None:
            return jsonify({
                'text': "Issue a new passcode and use it.", 
                'success': False
            })
        if registered.timeLimit < datetime.datetime.now():
            return jsonify({
                'text': "Issue a new passcode and use it.",
                'success': False
            })
        if registered.passcode != passcode:
            return jsonify({
                'text': "Incorrect passcode.",
                'success': False
            })
        if not DBaccess.clear():
            return jsonify({
                'text': "Data base error.",
                'success': False
            })
        
        pM.remove(user.id)
        return jsonify({
            'text': "All of the score data were cleared.",
            'success': True
        })
    return "You don't have the authority to access."

@module_admin.route('/issueCode', methods=['GET'])
@flask_login.login_required
def issueCode():
    user = flask_login.current_user
    if user.role == 'admin':
        timeLimit=pM.issue(user.id)
        return jsonify({'text': "A new passcode is issued. Effective until "+timeLimit.strftime('%Y/%m/%d %H:%M:%S')})
    return "You don't have the authority to access."

