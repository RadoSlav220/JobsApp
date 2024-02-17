from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import *
from enums.user_type import UserType

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(USER_NAME_MAXIMUM_LENGTH), unique=False, nullable=False)
    username = db.Column(db.String(USER_USERNAME_MAXIMUM_LENGTH), unique=True, nullable=False)
    password = db.Column(db.String(USER_PASSWORD_MAXIMUM_LENGTH), unique=False, nullable=False)
    email = db.Column(db.String(USER_EMAIL_MAXIMUM_LENGTH), unique=True, nullable=False)
    user_type = db.Column(db.Enum(UserType), unique=False, nullable=False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(JOB_TITLE_MAXIMUM_LENGTH), unique=False, nullable=False)
    company_name = db.Column(db.String(JOB_COMPANY_NAME_MAXIMUM_LENGTH), unique=False, nullable=False)
    recruiter_id = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(JOB_DESCRIPTION_MAXIMUM_LENGTH), unique=False, nullable=False)
    salary_lower_bound = db.Column(db.Integer, unique=False, nullable=False)
    salary_upper_bound = db.Column(db.Integer, unique=False, nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()