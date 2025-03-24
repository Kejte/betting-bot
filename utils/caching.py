import redis
import json

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

def cache_forks(forks: list[dict], bookers: str):
    for index, item in enumerate(forks):
        serialized_dict = json.dumps(item)
        redis_client.rpush(bookers,serialized_dict)
    redis_client.expire(bookers,300)

def get_cached_fork_data(bookers):
    forks = redis_client.lrange(bookers,0,-1)
    deserialized_forks  = [json.loads(fork.decode('utf-8')) for fork in forks]
    return deserialized_forks

def cache_profile(tg_id: int):
    redis_client.set(name=tg_id,value='auth')

def check_cached_user(tg_id: int):
        
        if redis_client.get(tg_id) == None:
            cache_profile(tg_id=tg_id)
            redis_client.expire(tg_id,86400)
            return False
        
        return True


    