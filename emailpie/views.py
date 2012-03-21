import simplejson

from emailpie import app
from emailpie.utils import EmailChecker
from emailpie.throttle import should_be_throttled

from flask import request, render_template, Response


@app.route('/', methods=['GET'])
def docs():
    return render_template('index.html')


@app.route('/v1/check', methods=['GET'])
def check():
    email = request.args.get('email', None)

    response = dict(success=True, errors=[], didyoumean=None)

    if should_be_throttled(request.remote_addr):
        return Response(simplejson.dumps(['throttled']),
            status_code=403,
            mimetype='application/json')

    if not email:
        response['errors'] += [dict(
                    severity=10,
                    message='Please provide an email address.')]
    else:
        validator = EmailChecker(email)
        response['errors'] = validator.validate()
        response['didyoumean'] = validator.didyoumean()

    for error in response['errors']:
        if error['severity'] > 5:
            response['success'] = False

    return Response(simplejson.dumps(response, indent=2),
        mimetype='application/json')
