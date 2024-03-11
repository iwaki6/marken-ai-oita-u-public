# ChatGPT Marking System of English Speaking Test for Medical Students

## Features
- **Deployment Options:** Run the software either locally or deploy it on the cloud platform *Render* for convenient accessibility.

## How to Use
This project provides a simple scoring system for English speaking on the web utlizing OpenAI chatGPT. 
You can use it by just accessing the root URL of the service with your browser. 
While the top page asks a password, no password is needed for the initial setting.
User's action and the response from chatGPT are registered in a database.
If you make a superuser account, you can access a management screen (/admin_world) which provides a simple access to the database.
(If you want to register a superuser, check password.py under the library folder.)

You can use, modify, redistribute these files freely.
This project is based on the repository https://github.com/hayashik/chatgpt-conversation-training-tool .

### Installation

**Prerequisites:**
 - Python 3.12.2
 - flask == 3.0.2
 - flask_cors == 4.0.0
 - flask_login == 0.6.3
 - flask_wtf == 1.2.1
 - openai == 1.13.3
 - openpyxl == 3.1.2
 - pandas == 2.2.1
 - pymongo[srv] == 4.6.2
 - bcrypt == 4.1.2
 - email_validator == 2.1.1

**Third Party Service:**
# You need to have accounts for the following services:
OpenAI
MongoDB at ATLAS
Outlook Mail

**Environment Variables:**
MARKEN_APP_KEY         # Arbitrary secret key.
OPENAI_API_KEY         # openai.OpenAI() uses this key implicitly. Get from OpenAI.
ATLAS_URI              # URI to access your database in MongoDB Cloud
MARKEN_MAIL_ADDRESS    # Your email address in Outlook Mail 
MARKEN_MAIL_PASSWORD   # Your account password in Outlook Mail

**Collections to be in your database:**
scores                 # Empty collection which register user's actions and chatGPT response.
superusers             # Each document in this collection should have keys: "email", "password", "role".
                       # email is a superuser's email address, password is used to log in "/admin_world", and role must be "admin".
                       # You need to insert such a document manually for each superuser. Check also password.py under library folder.


To run the project locally, follow these steps:

1. Clone the repository to your local machine:
```
bash
cd your-repository
```

2. Configure your MongoDB account to accept the access from your current ip-address.

3. Run app.py
```python app.py```

4. Access your local host with your browser.
If you see the following message, please open the URL in your browser:
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:8080
Press CTRL+C to quit
```

5. If you want to use it in your local network, please ask the Network Administrator of your office.



To run the project with Render, follow these steps:

1. Make a new repository for your own project in gitHub and copy these files.

2. At *Render* website (https://render.com/), sign up with your gitHub account.

3. Sign in *Render* and configure a new web service linking with your gitHub account.

4. Usually, your web service is automatically deployed. However, you need to do the following:
-a Configure environment variables at your web service.
-b Configure your MongoDB account to accept the access from ip-addresses which your service is running on.

