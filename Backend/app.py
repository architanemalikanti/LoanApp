from db import db
from flask import Flask, request
from db import db
from db import BankerUser, User
import json
from db import create_BankUser
from db import create_User
from db import verify_credentials
from db import renew_session
from db import verify_session
from db import verify_credentialsBanker



app = Flask(__name__)
db_filename = "casca.db"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///casca.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQALCHEMY_ECHO"] = True

# Initialize the database
db.init_app(app)

#helper functions
def success_response(body, status=200):
    return json.dumps(body), status

def failure_response(error, status=404):
    return json.dumps({"error": error}), status


def extract_token(request):
    token=request.headers.get("Authorization")
    if token is None:
        return False, "Missing authorization header"
    token=token.replace("Bearer", "").strip()
    return True, token

#register a USER or BANKER...route. remember, it depends whether its a banker or a user. 
@app.route("/register/", methods=["POST"])
def register_banker():
    body = json.loads(request.data)
    role = body.get('role') #could be a user, or could be a banker. 

    if role == "user":
        #fullName, bankStatementURL, email, password
        fullName=body.get('fullName')
        bankStatementURL = body.get('bankStatementURL')
        email=body.get('email')
        password=body.get('password')
        created, user = create_User(fullName, bankStatementURL, email, password)

    if role == "banker":
        email=body.get('email')
        password=body.get('password')
        created, user= create_BankUser(email, password)

    if not created:
        return failure_response("User already exists", 403)
    
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })


#log in user route:
@app.route("/loginUser/", methods=["POST"])
def login():
    body = json.loads(request.data)
    email=body.get('email')
    password = body.get('password')

    valid_creds, user= verify_credentials(email, password)

    if not valid_creds:
        return failure_response("Invalid credentials")
    
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token

    })

#login bankuser route:
@app.route("/bankUser/", methods=["POST"])
def login():
    body = json.loads(request.data)
    email=body.get('email')
    password = body.get('password')

    valid_creds, user= verify_credentialsBanker(email, password)

    if not valid_creds:
        return failure_response("Invalid credentials")
    
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token

    })

#register log in route:
@app.route("/session/", methods=["POST"])
def update_session():
    success, update_token=extract_token(request)

    if not success:
        return failure_response(update_token)
    

    valid, user=renew_session(update_token)

    if not valid:
        return failure_response("Invalid update token")
    
    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })

#secret route
@app.route("/secret/", methods=["GET"])
def secret_message():
    success, session_token =extract_token(request)

    if not success:
        return failure_response(session_token)
    
    valid=verify_session(session_token)

    if not  valid:
        return failure_response("Invalid session token")
    
    return success_response("Hello World!")



#add a loan applicant route
@app.route("/adduser/", methods=["POST"])
def add_user():
    body = json.loads(request.data)

    

#retrieve data for a loan applicant
@app.route("/processusers/", methods=["POST"])
def process_users():

  





if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host="0.0.0.0", port=8000, debug=True)
