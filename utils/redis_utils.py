import redis

def init_redis():
    r = redis.Redis(host='127.0.0.1', port=6379, db=1)
    return r