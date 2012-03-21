from hashlib import md5
import time
import simplejson

from emailpie import settings
cache = settings.cache


def should_be_throttled(identifier, SECONDS=settings.THROTTLE_SECONDS,
                                    LIMIT=settings.THROTTLE_LIMIT):
    """
    Maintains a list of timestamps when the user accessed the api within
    the cache.

    Returns `False` if the user should NOT be throttled or `True` if
    the user should be throttled.
    """
    key = 'throttle-' + md5(identifier).hexdigest()

    # Make sure something is there.
    cache.setnx(key, '[]')

    # eed out anything older than the timeframe.
    minimum_time = int(time.time()) - SECONDS
    times = simplejson.loads(cache.get(key))
    times_accessed = [access for access in times if access >= minimum_time]

    # Check times accessed count.
    if len(times_accessed) >= LIMIT:
        return True

    # update times accessed
    times_accessed.append(int(time.time()))
    cache.set(key, simplejson.dumps(times_accessed))
    cache.expire(key, SECONDS)

    return False

def reset_throttle(identifier):
    key = 'throttle-' + md5(identifier).hexdigest()
    cache.delete(key)
