
# Initialize Flask application
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from flask_cors import cross_origin
import flask_login

import os
import logging
import datetime

import chatGPTaccess
import DBaccess
import passcodeManager

APP_KEY = os.environ['MARKEN_APP_KEY'] # Set a secret word freely
PASSWORD0 = '' # Password for the main contents to restrict use by unexpected people. Set freely.

pM = passcodeManager.CodeEntries()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = APP_KEY

# Configure LoginManager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self,user_info) -> None:
        super().__init__()
        self.id = user_info['email']
        self.role = user_info['role']
        
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    user_info = DBaccess.inquire_user(email)
    if user_info is None:
        return 'Bad login'
    if request.form['password'] == user_info['password']:
        user = User(user_info)
        flask_login.login_user(user)
        if user.role == 'admin':
            return redirect(url_for('admin_world'))
        return redirect(url_for('protected'))

    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    # return 'Unauthorized', 401
    return redirect(url_for('login'))

###########################################################################
###########################################################################

# Management Screen for SuperUser

@app.route('/admin_world')
@flask_login.login_required
def admin_world():
    if flask_login.current_user.role == 'admin':
        return render_template('index_admin.html')
    return redirect(url_for('index'))

@app.route('/admin_world/export', methods=['POST'])
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

@app.route('/admin_world/download')
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

@app.route('/admin_world/clearDB', methods=['POST'])
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

@app.route('/admin_world/issueCode', methods=['GET'])
@flask_login.login_required
def issueCode():
    user = flask_login.current_user
    if user.role == 'admin':
        timeLimit=pM.issue(user.id)
        return jsonify({'text': "A new passcode is issued. Effective until "+timeLimit.strftime('%Y/%m/%d %H:%M:%S')})
    return "You don't have the authority to access."


###########################################################################
###########################################################################
# Dictionaries to store logs
answerLogs = {}
logs = {}  # A dictionary with usernames as keys and logs as values.
# assistant_logs = {}  # A dictionary that retains Assistant's response content with usernames as keys.

# Prompt
roletext = "You are teaching English conversation to Japanese freshmen."
prompt0 = "Give only a score for the next quiz out of 4 in the form n/4. Comment within 10 words: "

# Set up logging
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to recognize audio using OpenAI API
# @app.route('/recognize', methods=['POST'])
# def recognize():
#     return chatGPTaccess.recognize(request)

# Route for the chat functionality
@app.route('/chat', methods=['POST'])
@cross_origin()  # This will enable CORS for the /chat route only
def chat():
    data = request.get_json()
    questionID = data.get('QID')
    questionText = data.get('question')
    answerText = data.get('text')
    username = data.get('username')
    password = data.get('password')  

    # Check if username is provided
    if username is None or username.strip() == '':
        return jsonify({
            'text': "Please input username"
        })
    
    # Check if password is correct
    if PASSWORD0 != '' and PASSWORD0 != password:
        return jsonify({
            'text': "Please input the correct password"
        })

    # Check stored answer
    if questionText not in answerLogs:
        answerLogs[questionText] = []
    
    checkIfItExists = False
    for pooledAnswer in answerLogs[questionText]:
        if answerText == pooledAnswer[0]:
            checkIfItExists = True
            response_text = pooledAnswer[1]
            break

    if checkIfItExists:
        app.logger.info("For{}, recognizing of,{},{}, score,{}".format(questionText, username, answerText, response_text))
        return jsonify({
            'text': response_text
        })

    # Chat with chatGPT
    prompt = prompt0+"Question: "+questionText+" Answer: "+answerText
    response = chatGPTaccess.chat(roletext,prompt)
    if not response["success"]:
        return jsonify(text=response["text"])

    # Log Assistant's answer
    answerLogs[questionText].append([answerText,response["text"]])
    app.logger.info("For{}, recognizing of,{},{}, score,{}".format(questionText, username, answerText, response["text"]))
    user_score = int(response["text"][0])
    if not DBaccess.write(username,questionID,answerText,user_score):
        return jsonify(text="Database Error: Your score was not registered. Retry.")

    return jsonify({
        'text': response["text"]
    })




# Run the application if it is executed as the main script
if __name__ == '__main__':
    app.run(port=8080)
    #app.run()