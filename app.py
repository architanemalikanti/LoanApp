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
def loginUser():
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

#to check whether the user is signed in:
@app.route("/auth/status", methods=["GET"])
def auth_status():
    success, session_token = extract_token(request)
    print(f"Authorization header: {request.headers.get('Authorization')}")
    print(f"Extracted session token: {session_token}")

    if not success:
        return failure_response("Missing or invalid session token", 401)

    user = verify_session(session_token)
    print(f"User found: {user}")

    if not user:
        return failure_response("Invalid session token", 401)

    role = "banker" if isinstance(user, BankerUser) else "user"

    return success_response({
        "isSignedIn": True,
        "userId": user.user_id,
        "role": role
    })




#login bankuser route:
@app.route("/bankUser/", methods=["POST"])
def loginBanker():
    body = json.loads(request.data)
    email=body.get('email')
    password = body.get('password')

    valid_creds, user= verify_credentialsBanker(email, password)

    if not valid_creds:
        return failure_response("Invalid credentials")
    
    return success_response({
        "success": True,
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


#route for a user to apply to a loan
@app.route("/applyLoan/", methods=["POST"])
def apply_loan():
    body = json.loads(request.data)
    email=body.get('email')
    password = body.get('password')
    bankStatementURL=body.get('bankStatementURL')

    #call the ML model to instatiate the user's properties. (overall score, credit history).  
    #add the user to the loanApplication table. 
    
    return success_response({
        "success": True,
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token

    })
    

#route for a banker to recieve all loan applicants
@app.route("/allLoanApplicants/", methods=["GET"])
def loan_applicants():
    #return all users in the "LoanApplication" table. 


#route for a banker to reject a loan appliant
@app.route("/rejectApplicant/", methods=["POST"])
def reject_applicant():
    #route to reject an applicant. 
    #set the "acceptOrReject" field to FALSE: means rejected. true means accepted.


#route for a banker to accept a loan appliant
@app.route("/acceptApplicant/", methods=["POST"])
def accept_applicant():
    #route to reject an applicant. 
    #set the "acceptOrReject" field to TRUE: means rejected. true means accepted.


#route that displays a user's information: credit score, credit history, etc.
@app.route("/displayApplicant/", methods=["GET"])
def display_applicant():
    #route to display a user's information. 
    #return the user's information from the User table.



#route to return a user's ID. 


















  



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host="0.0.0.0", port=8000, debug=True)