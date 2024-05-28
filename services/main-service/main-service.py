# Flask
from flask import Flask, request
from werkzeug.exceptions import (
    NotFound,
    Unauthorized,
    Conflict,
    Forbidden,
    InternalServerError,
    BadRequest
)

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

# gRPC
import grpc
from generated import post_service_pb2
from generated import post_service_pb2_grpc
from generated import stat_service_pb2
from generated import stat_service_pb2_grpc

# kafka
from kafka import KafkaProducer
import json

# Misc
import os
import jwt
import hashlib
import sys
from datetime import datetime, timedelta
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
private_key = ""
public_key = ""
token_ttl_hours = 1

# setup kafka
kafka_producer = KafkaProducer(bootstrap_servers='kafka:9092',
                               value_serializer=lambda v: json.dumps(v).encode('utf-8'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    phone_number = db.Column(db.String(20), nullable=True, unique=True)


# JWT shenanigans
def encode_jwt(user_id):
    expiration_time = datetime.now() + timedelta(hours=token_ttl_hours)
    return jwt.encode(
        {'exp': expiration_time, 'user_id': user_id},
        private_key,
        algorithm='RS256'
    )


def decode_jwt(token):
    if not token:
        raise Unauthorized('Token is missing')
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


# Start server
def create_tables():
    with app.app_context():
        db.create_all()


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


def setup_stat_service():
    global stat_service_stub
    stat_service_addr = os.environ.get('STAT_SERVICE_ADDR')
    channel = grpc.insecure_channel(stat_service_addr)
    stat_service_stub = stat_service_pb2_grpc.StatServiceStub(channel)


def serve():
    create_tables()
    load_keys()
    setup_post_service()
    setup_stat_service()
    if __name__ == "__main__":
        app.run()


# ----- Helpers -----


def get_header(request, header: str):
    res = request.headers.get(header)
    if not res:
        raise BadRequest(f'No {header} passed')
    return res


def get_post_id(request):
    return int(get_header(request, 'post_id'))


# ----- Routes -----


@app.route('/register', methods=['POST'])
def register():
    request_body = request.json
    username = request_body.get('username')
    password = request_body.get('password')

    try:
        new_user = User(username=username,
                        password=hash_password(username, password))
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User has been registered successfully'}
    except IntegrityError:
        raise Conflict('User already exists')


@app.route('/login', methods=['POST'])
def login():
    request_body = request.json
    username = request_body.get('username')
    password = request_body.get('password')

    user = User.query.filter_by(
        username=username, password=hash_password(username, password)).first()
    if not user:
        raise Forbidden('Invalid username or password')

    return {
        'auth_token': encode_jwt(user.id),
        'message': 'Authentication successful, token is granted'
    }


@ app.route('/update-user-info', methods=['PUT'])
def update_user_info():
    user_id = decode_jwt(request.headers.get('Authorization'))
    request_body = request.json

    user = User.query.filter_by(id=user_id).first()
    user.first_name = request_body.get('first_name', user.first_name)
    user.last_name = request_body.get('last_name', user.last_name)
    user.date_of_birth = request_body.get('date_of_birth', user.date_of_birth)
    user.email = request_body.get('email', user.email)
    user.phone_number = request_body.get('phone_number', user.phone_number)

    db.session.commit()
    return {'message': "User's personal info successfully updated"}


@ app.route('/create-post', methods=['POST'])
def create_post():
    user_id = decode_jwt(request.headers.get('Authorization'))
    request_body = request.json
    content = request_body.get('content')

    grpc_request = post_service_pb2.CreatePostRequest(
        author_id=user_id, content=content)
    response = post_service_stub.CreatePost(grpc_request)

    return {
        'post_id': response.post_id,
        'message': 'Post created successfully!'
    }


@app.route('/update-post', methods=['PUT'])
def update_post():
    user_id = decode_jwt(request.headers.get('Authorization'))
    post_id = get_post_id(request)
    request_body = request.json
    content = request_body.get('content')

    try:
        grpc_request = post_service_pb2.UpdatePostRequest(
            user_id=user_id,
            post_id=post_id,
            content=content
        )
        response = post_service_stub.UpdatePost(grpc_request)
        return {'message': 'Post updated successfully!'}
    except grpc.RpcError as e:
        status_code = e.code()
        error_message = e.details()
        if status_code == grpc.StatusCode.NOT_FOUND:
            raise NotFound(error_message)
        elif status_code == grpc.StatusCode.PERMISSION_DENIED:
            raise Forbidden(error_message)
        raise InternalServerError()


@app.route('/delete-post', methods=['DELETE'])
def delete_post():
    user_id = decode_jwt(request.headers.get('Authorization'))
    post_id = get_post_id(request)

    try:
        grpc_request = post_service_pb2.DeletePostRequest(
            user_id=user_id,
            post_id=post_id,
        )
        response = post_service_stub.UpdatePost(grpc_request)
        if response.success:
            return {'message': 'Post deleted successfully!'}
    except grpc.RpcError as e:
        status_code = e.code()
        error_message = e.details()
        if status_code == grpc.StatusCode.NOT_FOUND:
            raise NotFound(error_message)
        elif status_code == grpc.StatusCode.PERMISSION_DENIED:
            raise Forbidden(error_message)
        raise InternalServerError()


@app.route('/get-post', methods=['GET'])
def get_post():
    post_id = get_post_id(request)

    try:
        grpc_request = post_service_pb2.GetPostByIdRequest(
            post_id=post_id,
        )
        response = post_service_stub.GetPostById(grpc_request)

        return {
            'author': response.author_id,
            'content': response.content,
        }
    except grpc.RpcError as e:
        status_code = e.code()
        error_message = e.details()
        if status_code == grpc.StatusCode.NOT_FOUND:
            raise NotFound(error_message)
        elif status_code == grpc.StatusCode.PERMISSION_DENIED:
            raise Forbidden(error_message)
        raise InternalServerError()


@app.route('/get-posts', methods=['GET'])
def get_posts():
    user_id = int(get_header(request, 'user-id'))
    posts_read = int(get_header(request, 'starting-post'))
    k_page_size = int(get_header(request, 'want-to-read'))
    posts = []

    grpc_request = post_service_pb2.GetPostsRequest(
        user_id=user_id,
        posts_read=posts_read,
        want_to_read=k_page_size,
    )
    response = post_service_stub.GetPosts(grpc_request)
    for post in response.posts:
        posts.append({
            'post_id': post.post_id,
            'author': post.author_id,
            'content': post.content,
        })

    return {'posts': posts}


@app.route('/view-post', methods=['PUT'])
def view_post():
    user_id = decode_jwt(request.headers.get('Authorization'))
    post_id = int(get_header(request, 'post-id'))
    kafka_producer.send('events', value={
        "event": "view",
        "user_id": int(user_id),
        "post_id": int(post_id),
    })
    return {}


@app.route('/like-post', methods=['PUT'])
def like_post():
    user_id = decode_jwt(request.headers.get('Authorization'))
    post_id = int(get_header(request, 'post-id'))
    kafka_producer.send('events', value={
        "event": "like",
        "user_id": int(user_id),
        "post_id": int(post_id),
    })
    return {'message': 'Post like event sent to Kafka'}


@app.route('/post-stats', methods=['GET'])
def get_post_stats():
    post_id = int(get_header(request, 'post-id'))
    grpc_request = stat_service_pb2.GetPostStatsRequest(post_id=post_id)
    grpc_response = stat_service_stub.GetPostStats(grpc_request)
    return {
        'post_id': grpc_response.post_id,
        'views': grpc_response.views,
        'likes': grpc_response.likes
    }


@app.route('/top-posts', methods=['GET'])
def get_top_posts():
    sort_by = request.args.get('sort_by', 'likes')
    grpc_request = stat_service_pb2.GetTopPostsRequest(sort_by=sort_by)
    grpc_response = stat_service_stub.GetTopPosts(grpc_request)
    posts = [{'post_id': post.post_id, 'count': post.count}
             for post in grpc_response.posts]
    return {'posts': posts}


@app.route('/top-users', methods=['GET'])
def get_top_users():
    grpc_request = stat_service_pb2.GetTopUsersRequest()
    grpc_response = stat_service_stub.GetTopUsers(grpc_request)
    users = [{'user_id': user.user_id, 'likes_count': user.likes_count}
             for user in grpc_response.users]
    return {'users': users}


serve()
