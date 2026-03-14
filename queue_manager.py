import redis
import json
import os

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), decode_responses=True)


def enqueue_email(email_data):
    r.rpush(os.getenv("REDIS_QUEUE"), json.dumps(email_data))


def dequeue_email():
    data = r.blpop(os.getenv("REDIS_QUEUE", "email_queue"))
    if data:
        return json.loads(data[1])
    return None
