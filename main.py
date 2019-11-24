import bottle
import appcode
import json

@bottle.route("/")
def index():
	return bottle.static_file('index.html', root = '')

@bottle.route("/script.js")
def script():
	return bottle.static_file('script.js', root = '')

@bottle.route("/styles.css")
def script():
	return bottle.static_file('styles.css', root = '')

@bottle.route('/pie')
def year():
	return(json.dumps(appcode.makePie()))

@bottle.route('/table')
def year():
	return(json.dumps(appcode.makeTable()))

@bottle.post('/send')
def show_graph():
	content = bottle.request.body.read()
	content = content.decode()
	return (appcode.receive_year(content)) 

bottle.run(debug = True)