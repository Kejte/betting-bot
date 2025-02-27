import redis
import json

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

def cache_forks(forks: list[dict], bookers: str):
    redis_client.set(bookers, json.dump(forks),300)

def get_cached_user_data(bookers, forks: list[dict]):
    cached_data = redis_client.get(bookers)
    if cached_data:
        return json.loads(cached_data)
    else:
        cache_forks()
    