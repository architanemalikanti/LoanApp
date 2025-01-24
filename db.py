from flask_sqlalchemy import SQLAlchemy
import datetime
import hashlib
import os
import bcrypt

db = SQLAlchemy()

#class for a registered user at Goldman Sachs. 
class BankerUser(db.Model):
    #name of model:
    __tablename__= "bankerusers"
    #user information:
    user_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    password_digest = db.Column(db.String, nullable=False)
    #session information:
    session_token = db.Column(db.String, nullable=False)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    #now we need to initialize this object and serialize it
    #initialize:
    def __init__(self, **kwargs):
        """
        initialize an assignment object
        """
        self.email=kwargs.get("email", "")
        self.password_digest= bcrypt.hashpw(kwargs.get("password").encode("utf-8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    #used to randomly generate/update session tokens:
    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()
    
    def renew_session(self):
        self.session_token=self._urlsafe_base_64()
        self.session_expiration=datetime.datetime.now()+datetime.timedelta(days=1)
        self.update_token=self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password_digest)
    
    #checks if session token is valid and hasnt expired:
    def verify_session_token(self, session_token):
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration
    
    def verify_update_token(self, update_token):
        return update_token == self.update_token
    

    #simple serialize method:
    def simple_serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    

def create_BankUser(email, password):
    existing_bankUser= BankerUser.query.filter(BankerUser.email==email).first()
    if existing_bankUser:
        return False, None
    
    newBankUser=BankerUser(email=email, password=password)
    db.session.add(newBankUser)
    db.session.commit()
    return True, newBankUser

def verify_credentials(email, password):
    existing_banker= BankerUser.query.filter(BankerUser.email==email).first()
    if not existing_banker:
        return False, None
    
    return existing_banker.verify_password(password), existing_banker

def renew_session(update_token):
    existing_barista= BankerUser.query.filter(BankerUser.update_token==update_token).first()
    if not existing_barista:
        return False, None
    
    existing_barista.renew_session()
    db.session.commit()
    return True, existing_barista


def verify_session(session_token):
    return BankerUser.query.filter(BankerUser.session_token==session_token).first()




#class for a LOAN APPLICANT. 
class User(db.Model):
    #name of model
    __tablename__ = "users"
    #user information:
    user_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullName = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    bankStatementURL = db.Column(db.String, nullable=False)
    password_digest = db.Column(db.String, nullable=False)
    #application- relationship
    applications = db.relationship("LoanApplication", cascade="delete")



    #financial health information, which will be initialized using the ML model. 
    #session information:
    session_token = db.Column(db.String, nullable=False)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    #initialize:
    def __init__(self, **kwargs):
        """
        initialize an assignment object
        """
        self.fullName=kwargs.get("fullName", "")
        self.email=kwargs.get("email", "")
        self.bankStatementURL=kwargs.get("bankStatementURL", "")
        self.password_digest= bcrypt.hashpw(kwargs.get("password").encode("utf-8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    #used to randomly generate/update session tokens:
    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()
    
    def renew_session(self):
        self.session_token=self._urlsafe_base_64()
        self.session_expiration=datetime.datetime.now()+datetime.timedelta(days=1)
        self.update_token=self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password_digest)
    
    #checks if session token is valid and hasnt expired:
    def verify_session_token(self, session_token):
        return session_token == self.session_token and datetime.datetime.now() < self.session_expiration
    
    def verify_update_token(self, update_token):
        return update_token == self.update_token
        

    #serialize method
    def serialize(self):
        return{
            "id": self.user_id,
            "fullName": self.fullName,
            "email": self.email,
            "bankStatementURL": self.bankStatementURL,
            "applications": [s.serialize() for s in self.applications]
        }

def create_User(fullName, bankStatementURL, email, password):
    existing_User= User.query.filter(User.email==email).first()
    if existing_User:
        return False, None
    
    #use the ML model HERE to instatiate the new user with ML model outputs. 
    #right down below in our initializer:
    newUser=User(fullName=fullName, email=email, password=password, bankStatementURL=bankStatementURL)
    db.session.add(newUser)
    db.session.commit()
    return True, newUser

#for User login:
def verify_credentials(email, password):
    existing_user= User.query.filter(BankerUser.email==email).first()
    if not existing_user:
        return False, None
    
    return existing_user.verify_password(password), existing_user

def verify_credentialsBanker(email, password):
    existing_user= BankerUser.query.filter(BankerUser.email==email).first()
    if not existing_user:
        return False, None
    
    return existing_user.verify_password(password), existing_user


def renew_session(update_token):
    existing_user= User.query.filter(User.update_token==update_token).first()
    if not existing_user:
        return False, None
    
    existing_user.renew_session()
    db.session.commit()
    return True, existing_user


def verify_session(session_token):
    # Check for the session token in the BankerUser table first
    user = BankerUser.query.filter(BankerUser.session_token == session_token).first()
    if user:
        return user
    
    # If not found, check in the User table
    user = User.query.filter(User.session_token == session_token).first()
    return user


#a class for loan applications: many loan application
#class for an assignment:
class LoanApplication(db.Model):
    #name of model:
    __tablename__= "loanApplication"

    #columns:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateApplied = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Correct column name


    # Initialize
    def __init__(self, **kwargs):
        self.dateApplied = kwargs.get("dateApplied", None)
        self.user_id = kwargs.get("user_id")


    # Serialize
    def serialize(self):
        return {
            "id": self.id,
            "dateApplied": self.dateApplied.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": self.user_id
        }
