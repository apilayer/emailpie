import simplejson

from emailpie import app
from emailpie.utils import EmailChecker

from flask import request


@app.route('/', methods=['GET'])
def docs():
    return 'Hello World!'


@app.route('/v1/check', methods=['GET'])
def check():
    email = request.args.get('email', None)

    response = dict(success=True, errors=[])

    if not email:
        response['errors'] += [dict(
                    severity=10,
                    message='Please provide an email address.')]
    else:
        validator = EmailChecker(email)
        response['errors'] = validator.validate()

    for error in response['errors']:
        if error['severity'] > 5:
            response['success'] = False

    return simplejson.dumps(response)
