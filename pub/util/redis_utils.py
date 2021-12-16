import secrets
import redis
from .log_utils import logger as LOG
import os
# ==================== REDIS ===========================================
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_URL = "redis://{host}:{port}".format(host=REDIS_HOST, port=REDIS_PORT)

def generate_rand_token():
    return secrets.token_urlsafe()

def save_value_to_set_list(list_name, data):
    try:
        redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        redisClient.sadd(list_name, data)
        return True
    except Exception as e:
        LOG.exception(e)
        return False
def is_data_in_set_list(list_name, data):
    try:
        redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        isExist =redisClient.sismember(list_name, data)
        if isExist:
            return True
        return False
    except Exception as e:
        LOG.info(e)
        return False
def count_data_in_set_list(list_name):
    try:
        redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        count =redisClient.scard(list_name)
        return count
    except Exception as e:
        LOG.info(e)
        return -1
def get_data_in_set_list(list_name):
    try:
        redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        datas =redisClient.smembers(list_name)
        if datas:
            return [str(id) for id in datas]
        else:
            return None
    except Exception as e:
        LOG.info(e)
        return None
def clear_data_in_set_list(list_name):
    try:
        redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        redisClient.delete(list_name)
        return True
    except Exception as e:
        LOG.info(e)
        return False

def get_value_key(key):
    try:
        redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf-8", decode_responses=True)
        data =redisClient.get(key)
        return data
    except Exception as e:
        LOG.info(e)
        return None
def save_value_key(key, data, ttl=1000000):
    try:
        redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        redisClient.set(key, data, ex=ttl)
        return True
    except Exception as e:
        LOG.exception(e)
        return False