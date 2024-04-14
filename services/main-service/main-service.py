from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest, Conflict, Forbidden

import os
import jwt
import hashlib
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
private_key = ""
public_key = ""

private_key_path = os.environ.get('PRIVATE_KEY_PATH')
public_key_path = os.environ.get('PUBLIC_KEY_PATH')

with open(private_key_path, 'rb') as file:
    private_key = file.read()
with open(public_key_path, 'rb') as file:
    public_key = file.read()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    phone_number = db.Column(db.String(20), nullable=True, unique=True)


def encode_jwt(username):
    return jwt.encode({'username': username}, private_key, algorithm='RS256')


def decode_jwt(token):
    try:
        payload = jwt.decode(token, public_key, algorithms=['RS256'])
        return payload['username']
    except:
        raise BadRequest('Invalid token')


def hash_password(username, password):
    hashed_password = hashlib.md5(
        (password + username).encode('utf-8')).hexdigest()
    return hashed_password


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    print(
        f"!register, username: {username}, password: {password}", file=sys.stderr)

    try:
        new_user = User(username=username,
                        password=hash_password(username, password))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User has been registered successfully'})
    except IntegrityError:
        raise Conflict('User already exists')


@app.route('/update-user-info', methods=['PUT'])
def update_user_info():
    data = request.json
    auth_token = data.get('auth_token')
    username = decode_jwt(auth_token)
    print(f"!update-user-info, username: {username}", file=sys.stderr)

    user = User.query.filter_by(username=username).first()
    if (user is None):
        raise NotFound('User not found')
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
    user.email = data.get('email', user.email)
    user.phone_number = data.get('phone_number', user.phone_number)

    db.session.commit()
    return jsonify({'message': "User's personal info successfully updated"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(
        username=username, password=hash_password(username, password)).first()
    if not user:
        raise Forbidden('Invalid username or password')

    print(
        f"!login, username: {username}, password: {password}", file=sys.stderr)

    return jsonify({
        'auth_token': encode_jwt(username),
        'message': 'Authentication successful! Token is granted'
    })


if __name__ == '__main__':
    app.run()
