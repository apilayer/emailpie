from gevent import monkey
monkey.patch_all()

import gevent.wsgi
from emailpie import app


ws = gevent.wsgi.WSGIServer(('', 24259), app)
ws.serve_forever()
