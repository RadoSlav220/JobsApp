import json
from flask import Flask, Request, jsonify, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

@app.route("/")
def home():
    return render_template('index.html', title='Home', user='Rado')

@app.route("/login")
def login():
    return render_template('login.html', title='Login')

def register_user(request: Request):
    username = request.form['username']
    password = request.form['password'] # TODO: Hash!
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Register')
    elif request.method == 'POST':
        register_user(request)
        return render_template('register.html', title='Register', message='Registered successfully!')
    else:
        return make_response("Error!", 400, {"Debug": "Error!"})

@app.route("/magic")
def read_data():
    users = User.query.all()
    result = '<h1>You hacked the database :O</h1>'
    for user in users:
        result += f'<h3>{user.id} {user.username} {user.password}</h3>'
    return result

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)