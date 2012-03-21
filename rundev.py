from gevent import monkey
monkey.patch_all()


from emailpie import app
app.run(debug=True)
