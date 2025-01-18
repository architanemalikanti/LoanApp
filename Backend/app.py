from db import db
from flask import Flask, request
from db import db
from db import Barista, ShiftLead, PastryPull
import json
from db import create_barista
from db import verify_credentials
from db import renew_session
from db import verify_session






app = Flask(__name__)
db_filename = "starbucks.db"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///starbucks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQALCHEMY_ECHO"] = True

# Initialize the database
db.init_app(app)

#helper functions

def success_response(body, status=200):
    return json.dumps(body), status

def failure_response(error, status=404):
    return json.dumps({"error": error}), status




@app.route("/compareusers/", methods=["POST"])
def compare_users():
    





if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host="0.0.0.0", port=8000, debug=True)
