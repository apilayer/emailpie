from emailpie import app, utils


@app.route('/v1/check', methods=['GET'])
def check():
    return 'Hello World!'
