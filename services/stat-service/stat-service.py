from kafka import KafkaConsumer
from clickhouse_driver import Client

import time
import json
import sys

time.sleep(10)
# setup kafka
consumer = KafkaConsumer('events',
                         bootstrap_servers='kafka:9092',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# setup clickhouse
client = Client(host='stat-service-db', port='9000')
client.execute(
    'CREATE TABLE IF NOT EXISTS likes (post_id UInt64, user_id UInt64) ENGINE MergeTree ORDER BY (post_id, user_id)')
client.execute(
    'CREATE TABLE IF NOT EXISTS views (post_id UInt64, user_id UInt64) ENGINE MergeTree ORDER BY (post_id, user_id)')


# consume messages
print("Consuming messages", file=sys.stderr)
for message in consumer:
    event = message.value
    event_type = event['event']
    user_id = int(event['user_id'])
    post_id = int(event['post_id'])
    print(f"Event: {event}", file=sys.stderr)

    if event_type == 'view':
        client.execute('INSERT INTO views (post_id, user_id) VALUES',
                       [[post_id, user_id]])
    elif event_type == 'like':
        client.execute('INSERT INTO likes (post_id, user_id) VALUES',
                       [[post_id, user_id]])
