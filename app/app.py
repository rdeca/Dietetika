from bottle import Bottle, run, static_file, template

app = Bottle()


# statične datoteka, torej css/js/fonti
@app.get('/fonts/<filename:path>')
def fonts(filename):
    return static_file(filename, root='static/fonts/')

@app.get('/css/<filename:path>')
def css(filename):
    return static_file(filename, root='static/css/')

@app.get('/js/<filename:path>')
def js(filename):
    return static_file(filename, root='static/js/')



# routing
@app.route('/')
def index():
	return template("entry.tpl")




run(app, host='localhost', port=8080, reloader=True)