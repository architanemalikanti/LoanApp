from flask_sqlalchemy import SQLAlchemy
import datetime
import hashlib
import os
import bcrypt

db = SQLAlchemy()


#class for a Barista. 
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
