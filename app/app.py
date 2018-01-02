import bottle
import bottle.ext.sqlite
from bottle import Bottle, run, static_file, template, debug

app = Bottle()

#install db connection
plugin = bottle.ext.sqlite.Plugin(dbfile='./db/dietetika.sqlite')
app.install(plugin)


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

@app.route('/consumables')
def consumables(db):
	q = """SELECT c.id,
					c.title,
					c.calories,
					ct.title as consumable_type_title,
					ctp.title as consumable_type_parent_title,
					count(chn.nutrient_id) as nutrient_count 
			FROM consumable c 
				LEFT JOIN consumable_type ct ON (c.consumable_type_id = ct.id) 
				LEFT JOIN consumable_type_parent ctp ON (ct.consumable_type_parent_id = ctp.id)
				LEFT JOIN consumable_has_nutrient chn ON (chn.consumable_id = c.id)
			GROUP BY c.id
			ORDER BY c.id"""

	c = db.execute(q)
	r_consumables = c.fetchall()
	return template("consumables-list.tpl", consumables = r_consumables)

@app.route('/consumable/<consumable_id>')
def consumable(consumable_id):
	#TODO: q data in sqlite
	return template("consumables-list.tpl", {})

debug(True)
run(app, host='localhost', port=8080, reloader=True)