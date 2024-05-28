from kafka import KafkaConsumer
from clickhouse_driver import Client

# gRPC
import grpc
from generated.stat_service_pb2 import *
from generated.stat_service_pb2_grpc import StatServiceServicer, add_StatServiceServicer_to_server

# Misc
from concurrent import futures
import threading
import json
import time
import sys
import os

# setup clickhouse
client = Client(host='stat-service-db', port='9000')
client.execute(
    'CREATE TABLE IF NOT EXISTS likes (post_id UInt64, user_id UInt64) ENGINE MergeTree ORDER BY (post_id, user_id)')
client.execute(
    'CREATE TABLE IF NOT EXISTS views (post_id UInt64, user_id UInt64) ENGINE MergeTree ORDER BY (post_id, user_id)')


class StatService(StatServiceServicer):
    def __init__(self):
        self.client = client

    def GetPostStats(self, request, context):
        print("GetPostStats", file=sys.stderr)
        post_id = request.post_id
        views_count = self.client.execute(
            f'SELECT count() FROM views WHERE post_id = {post_id}')[0][0]
        likes_count = self.client.execute(
            f'SELECT count() FROM likes WHERE post_id = {post_id}')[0][0]
        return GetPostStatsResponse(post_id=post_id, views=views_count, likes=likes_count)

    def GetTopPosts(self, request, context):
        sort_by = request.sort_by
        if sort_by == "views":
            query = 'SELECT post_id, count() as count FROM views GROUP BY post_id ORDER BY count DESC LIMIT 5'
        else:
            query = 'SELECT post_id, count() as count FROM likes GROUP BY post_id ORDER BY count DESC LIMIT 5'

        rows = self.client.execute(query)
        posts = []
        for row in rows:
            post_id = row[0]
            count = row[1]
            posts.append(PostInfo(post_id=post_id, count=count))

        return GetTopPostsResponse(posts=posts)

    def GetTopUsers(self, request, context):
        query = 'SELECT user_id, count() as likes_count FROM likes GROUP BY user_id ORDER BY likes_count DESC LIMIT 3'
        rows = self.client.execute(query)
        users = []
        for row in rows:
            user_id = row[0]
            likes_count = row[1]
            users.append(UserInfo(user_id=user_id, likes_count=likes_count))

        return GetTopUsersResponse(users=users)


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_StatServiceServicer_to_server(StatService(), server)
    port = os.environ["STAT_SERVICE_PORT"]
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


def consume_kafka():
    consumer = KafkaConsumer('events',
                             bootstrap_servers='kafka:9092',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    print("Consuming messages", file=sys.stderr)
    for message in consumer:
        event = message.value
        event_type = event['event']
        user_id = int(event['user_id'])
        post_id = int(event['post_id'])
        print(f"Event: {event}", file=sys.stderr)

        if event_type == 'view':
            client.execute('INSERT INTO views (post_id, user_id) VALUES', [
                           [post_id, user_id]])
        elif event_type == 'like':
            client.execute('INSERT INTO likes (post_id, user_id) VALUES', [
                           [post_id, user_id]])


if __name__ == "__main__":
    time.sleep(10)
    # threading.Thread(target=serve_grpc).start()
    # threading.Thread(target=consume_kafka).start()
    serve_grpc()  # DEBUG
