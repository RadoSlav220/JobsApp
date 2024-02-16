from enum import Enum
import hashlib
from flask import Flask, Request, jsonify, redirect, render_template, request, make_response, url_for
from flask_sqlalchemy import SQLAlchemy

from exceptions.UserNotFoundError import UserNotFoundError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

PASSWORD_MINIMUM_LENGTH = 4
PASSWORD_MAXIMUM_LENGTH = 120
USERNAME_MAXIMUM_LENGTH = 80
NAME_MAXIMUM_LENGTH = 120

LOGGED_USER = None

class UserType(Enum):
    RECRUITER = 'recruiter'
    APPLICANT = 'applicant'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(NAME_MAXIMUM_LENGTH), unique=False, nullable=False)
    username = db.Column(db.String(USERNAME_MAXIMUM_LENGTH), unique=True, nullable=False)
    password = db.Column(db.String(PASSWORD_MAXIMUM_LENGTH), unique=False, nullable=False)
    user_type = db.Column(db.Enum(UserType), unique=False, nullable=False)

@app.route("/")
def home():
    if LOGGED_USER:
        return make_response(render_template('index.html', title='Home', user=LOGGED_USER))
    else:
        return make_response(render_template('index.html', title='Home', message='Login first!'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    global LOGGED_USER
    if request.method == 'GET' and LOGGED_USER:
        return make_response("You must logout first.", 400)
    elif request.method == 'GET':
        return make_response(render_template('login.html', title='Login'))
    elif request.method == 'POST':
        try:
            login_user(request)
            return redirect(url_for('home'))
        except ValueError as error:
            return make_response(render_template('login.html', title='Login', message=str(error)), 400)
        except UserNotFoundError as error:
            return make_response(render_template('login.html', title='Login', message=str(error)), 404)
    else:
        return make_response("Method not allowed!", 405)


@app.route("/logout", methods=['GET'])
def logout():
    global LOGGED_USER
    if LOGGED_USER:
        LOGGED_USER = None
        return redirect(url_for('home'))
    else:
        return make_response("You are not logged in.", 400)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET' and LOGGED_USER:
        return make_response("You must logout first.", 400)
    if request.method == 'GET':
        return make_response(render_template('register.html', title='Register'))
    elif request.method == 'POST':
        try:
            register_user(request)
            return make_response(render_template('register.html', title='Register', message='Registered successfully!'))
        except ValueError as error:
            return make_response(render_template('register.html', title='Register', message=str(error)), 400)
    else:
        return make_response("Method not allowed!", 405)


@app.route("/magic")
def read_data():
    users = User.query.all()
    result = ''
    for user in users:
        result += f'<h3>{user.id} {user.name} {user.username} {user.password} {user.user_type}</h3>'
    return result


def consistent_hash(input_string) -> str:
    input_bytes = input_string.encode('utf-8')
    hashed_bytes = hashlib.sha256(input_bytes).digest()
    hashed_hex = hashlib.sha256(input_bytes).hexdigest()
    return hashed_hex


def login_user(request: Request) -> User: 
    global LOGGED_USER
    requestUsername = request.form.get('username')
    requestPassword = request.form.get('password')

    validate_username(requestUsername)
    validate_password(requestPassword)
    
    user = User.query.filter_by(username=requestUsername, password=consistent_hash(requestPassword)).first()
    if user:
        LOGGED_USER = user
        return user
    else:
        raise UserNotFoundError('Wrong username or password')


def validate_name(name: str) -> None:
    if name is None or name == '':
        raise ValueError('Missing name')
    
    if len(name) > NAME_MAXIMUM_LENGTH:
        raise ValueError('Name is too long')

def validate_username(username: str) -> None:
    if username is None or username == '':
        raise ValueError('Missing username')
    
    if len(username) > USERNAME_MAXIMUM_LENGTH:
        raise ValueError('Username is too long')

def validate_password(password: str) -> None:
    if password is None or password == '':
        raise ValueError('Missing password')

    if len(password) < PASSWORD_MINIMUM_LENGTH:
        raise ValueError('Password is too short')
    
    if len(password) > PASSWORD_MAXIMUM_LENGTH:
        raise ValueError('Password is too long')

def validate_user_type(user_type: str) -> None:
    if user_type is None or user_type == '':
        raise ValueError('Missing user type')

    if user_type != 'recruiter' and user_type != 'applicant':
        raise ValueError('Invalid user type')

def is_user_registered(username):
    return User.query.filter_by(username=username).first()

def register_user(request: Request):
    requestName = request.form.get('name')
    requestUsername = request.form.get('username')
    requestPassword = request.form.get('password')
    requestUserType = request.form.get('user_type')

    validate_name(requestName)
    validate_username(requestUsername)
    validate_password(requestPassword)
    validate_user_type(requestUserType)

    if is_user_registered(requestUsername):
        raise ValueError("Username is already taken")

    new_user = User(name=requestName, username=requestUsername, 
                    password=consistent_hash(requestPassword), user_type=UserType(requestUserType))
    db.session.add(new_user)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        # db.session.query(User).delete()
        # db.session.commit()
        db.create_all()
    app.run(debug=True)