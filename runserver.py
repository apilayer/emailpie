from gevent import monkey
monkey.patch_all()

import gevent.wsgi
import werkzeug.serving

from emailpie import app


@werkzeug.serving.run_with_reloader
def runServer():
    ws = gevent.wsgi.WSGIServer(('', 24259), app)
    ws.serve_forever()

runServer()
