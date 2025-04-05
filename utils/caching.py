import redis
import json
import datetime
import pytz

def time_until_end_of_day():
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(moscow_tz)  
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)  
    time_remaining = end_of_day - now  
    return int(time_remaining.total_seconds())  

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

def cache_profile(tg_id: int, permission: str):
    redis_client.set(name=tg_id,value=f'auth_{permission}')
    redis_client.expire(tg_id,time_until_end_of_day())

def check_cached_user(tg_id: int):
        
        if redis_client.get(tg_id) == None:
            return False
        
        return True

def get_cached_user(tg_id: int) -> str:
    return str(redis_client.get(tg_id))

     