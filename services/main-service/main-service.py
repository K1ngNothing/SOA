# Flask
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import (
    Unauthorized,
    Conflict,
    Forbidden,
    InternalServerError
)

# gRPC
import grpc
from generated import post_service_pb2
from generated import post_service_pb2_grpc

# Misc
import os
import jwt
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
private_key = ""
public_key = ""
token_ttl_hours = 1


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    phone_number = db.Column(db.String(20), nullable=True, unique=True)


def encode_jwt(user_id):
    expiration_time = datetime.now() + timedelta(hours=token_ttl_hours)
    return jwt.encode(
        {'exp': expiration_time, 'user_id': user_id},
        private_key,
        algorithm='RS256'
    )


def decode_jwt(token):
    try:
        payload = jwt.decode(token, public_key, algorithms=['RS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise Unauthorized('Token is expired')
    except:
        raise Unauthorized('Invalid token')


def hash_password(username, password):
    hashed_password = hashlib.md5(
        (password + username).encode('utf-8')).hexdigest()
    return hashed_password


def load_keys():
    global private_key, public_key
    private_key_path = os.environ.get('PRIVATE_KEY_PATH')
    public_key_path = os.environ.get('PUBLIC_KEY_PATH')

    with open(private_key_path, 'rb') as file:
        private_key = file.read()
    with open(public_key_path, 'rb') as file:
        public_key = file.read()


def setup_post_service():
    global post_service_stub
    post_service_addr = os.environ.get('POST_SERVICE_ADDR')
    channel = grpc.insecure_channel(post_service_addr)
    post_service_stub = post_service_pb2_grpc.PostServiceStub(channel)

# ----- Routes -----


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        new_user = User(username=username,
                        password=hash_password(username, password))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User has been registered successfully'})
    except IntegrityError:
        raise Conflict('User already exists')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(
        username=username, password=hash_password(username, password)).first()
    if not user:
        raise Forbidden('Invalid username or password')

    return jsonify({
        'auth_token': encode_jwt(user.id),
        'message': 'Authentication successful! Token is granted'
    })


@app.route('/update-user-info', methods=['PUT'])
def update_user_info():
    data = request.json
    auth_token = data.get('auth_token')
    user_id = decode_jwt(auth_token)

    user = User.query.filter_by(id=user_id).first()
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
    user.email = data.get('email', user.email)
    user.phone_number = data.get('phone_number', user.phone_number)

    db.session.commit()
    return jsonify({'message': "User's personal info successfully updated"})


@app.route('/create-post', methods=['POST'])
def create_post():
    data = request.json
    user_id = decode_jwt(data.get('auth_token'))
    content = data.get('content')

    grpc_request = post_service_pb2.CreatePostRequest(
        author_id=user_id, content=content)
    response = post_service_stub.CreatePost(grpc_request)

    return jsonify({
        'post_id': response.post_id,
        'message': 'Post created successfully!'
    })


@app.route('/update-post', methods=['PUT'])
def update_post():
    data = request.json
    user_id = decode_jwt(data.get('auth_token'))
    post_id = data.get('post_id')
    content = data.get('content')

    grpc_request = post_service_pb2.UpdatePostRequest(
        user_id=user_id,
        post_id=post_id,
        content=content
    )
    response = post_service_stub.UpdatePost(grpc_request)
    if response.success:
        return jsonify({
            'message': 'Post updated successfully!'
        })
    else:
        # TODO: get error from grpc
        raise InternalServerError('Failed to update post')


@app.route('/delete-post', methods=['PUT'])
def delete_post():
    data = request.json
    user_id = decode_jwt(data.get('auth_token'))
    post_id = data.get('post_id')

    grpc_request = post_service_pb2.DeletePostRequest(
        user_id=user_id,
        post_id=post_id,
    )
    response = post_service_stub.UpdatePost(grpc_request)
    if response.success:
        return jsonify({
            'message': 'Post deleted successfully!'
        })
    else:
        # TODO: get error from grpc
        raise InternalServerError('Failed to delete post')


@app.route('/get-post', methods=['PUT'])
def get_post():
    data = request.json
    user_id = decode_jwt(data.get('auth_token'))
    post_id = data.get('post_id')

    grpc_request = post_service_pb2.GetPostByIdRequest(
        user_id=user_id,
        post_id=post_id,
    )
    response = post_service_stub.GetPostById(grpc_request)

    # TODO: check error from grpc
    return jsonify({
        'author': response.author_id,
        'content': response.content,
    })


@app.route('/get-posts', methods=['PUT'])
def get_posts():
    k_page_size = 1

    data = request.json
    user_id = decode_jwt(data.get('auth_token'))
    posts_read = 0
    posts = []
    while True:
        grpc_request = post_service_pb2.GetPostsRequest(
            user_id=user_id,
            posts_read=posts_read,
            want_to_read=k_page_size,
        )
        response = post_service_stub.GetPosts(grpc_request)
        posts_read += len(response.posts)
        if len(response.posts) == 0:
            break

        for post in response.posts:
            posts.append({
                'post_id': post.post_id,
                'author': post.author_id,
                'content': post.content,
            })

    return jsonify({
        'posts': posts,
    })


def serve():
    load_keys()
    setup_post_service()
    if __name__ == "__main__":
        app.run()


# no __name__ == "__main__" d.t. Flask shenanigans
serve()
