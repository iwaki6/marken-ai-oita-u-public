from flask import Blueprint, render_template, request, jsonify, current_app
from flask_cors import cross_origin

import library.chatGPTaccess as chatGPTaccess
import library.DBaccess as DBaccess

module_main = Blueprint('app_main', __name__, url_prefix='')

# Password for the main contents to restrict use by unexpected people. Set freely.
PASSWORD0 = 'maruchan' 

# Dictionaries to store logs
answerLogs = {}
logs = {}  # A dictionary with usernames as keys and logs as values.
# assistant_logs = {}  # A dictionary that retains Assistant's response content with usernames as keys.

# Prompt
roletext = "You are teaching English conversation to Japanese freshmen."
prompt0 = "Give only a score for the next quiz out of 4 in the form n/4. Comment within 10 words: "

# Route for the home page
@module_main.route('/')
def index():
    return render_template('index.html')

# Route to recognize audio using OpenAI API
# @app.route('/recognize', methods=['POST'])
# def recognize():
#     return chatGPTaccess.recognize(request)

# Route for the chat functionality
@module_main.route('/chat', methods=['POST'])
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
            'text': "Please input username."
        })
    
    # Check if password is correct
    if PASSWORD0 != '' and PASSWORD0 != password:
        return jsonify({
            'text': "Please input the correct password."
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
        current_app.logger.info("For{}, recognizing of,{},{}, score,{}".format(questionText, username, answerText, response_text))
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
    current_app.logger.info("For{}, recognizing of,{},{}, score,{}".format(questionText, username, answerText, response["text"]))
    user_score = int(response["text"][0])
    if not DBaccess.write(username,questionID,answerText,user_score):
        return jsonify(text="Database Error: Your score was not registered. Retry.")

    return jsonify({
        'text': response["text"]
    })

