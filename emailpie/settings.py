GEVENT_CHECKS = True

THROTTLE_SECONDS = 60 * 60
THROTTLE_LIMIT = 1800

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


try:
    from settings_local import *
except ImportError:
    pass

import redis
cache = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB)