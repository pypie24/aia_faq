import json
import redis

from src.constants import BATCH_EMBEDDING_SIZE


redis_client = redis.Redis(host="redis", port=6379, db=1)


def push_to_queue(item: dict):
    redis_client.rpush("embedding_queue", json.dumps(item))


def pop_all_from_queue() -> list:
    batches = []
    while batch := redis_client.lpop("embedding_queue", BATCH_EMBEDDING_SIZE):
        items = [json.loads(item) for item in batch]
        batches.append(items)
    return batches
