GEVENT_CHECKS = True

THROTTLE_SECONDS = 60 * 60
THROTTLE_LIMIT = 1800

import redis
cache = redis.StrictRedis(host='localhost', port=6380, db=13)