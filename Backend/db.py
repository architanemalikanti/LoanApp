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
    bankStatementURL = db.Column(db.String, nullable=False)
    #financial health variables, which will be initialized using the ML model. 



    #initialize:
    def __init__(self, **kwargs):
        """
        initialize an assignment object
        """
        self.fullName=kwargs.get("fullName", "")
        self.bankStatementURL=kwargs.get("bankStatementURL", "")

   

    #serialize method
    def serialize(self):
        return{
            "id": self.user_id,
            "fullName": self.fullName,
            "bankStatementURL": self.bankStatementURL
        }
