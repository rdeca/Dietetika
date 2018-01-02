import bottle
import bottle.ext.sqlite
from bottle import Bottle, run, static_file, template, debug, redirect, request
import json

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
def consumable(consumable_id, db):
	q = """SELECT c.id, 
					c.title,
					ct.title as consumable_type_title,
					ctp.title as consumable_type_parent_title,
					c.calories 
				FROM consumable c 
				LEFT JOIN consumable_type ct ON (c.consumable_type_id = ct.id) 
				LEFT JOIN consumable_type_parent ctp ON (ct.consumable_type_parent_id = ctp.id) 
				WHERE c.id = '{id}'""".format(id = consumable_id)
	c = db.execute(q)
	consumable = c.fetchone()
	q_nutrients = """SELECT n.id,
							n.title,
							nt.title as nutrient_type_title,
							chn.value  
						FROM consumable_has_nutrient chn 
							LEFT JOIN nutrient n ON (chn.nutrient_id = n.id)
							LEFT JOIN nutrient_type nt ON (n.nutrient_type_id = n.id)
						WHERE chn.consumable_id = '{id}'""".format(id = consumable_id)
	c = db.execute(q_nutrients)
	nutrients = c.fetchall()
	return template("consumable-details.tpl", c = consumable, n = nutrients)

@app.route('/consumable-delete/<id>')
def consumable_delete(id, db):
	q = "DELETE FROM consumable WHERE id = {id}".format(id = id)
	c = db.execute(q)
	if c.rowcount == 1:
		redirect('/consumables')
	else:
		redirect('/consumable/{id}'.format(id=id))


@app.route('/consumable-edit/<id>')
def consumable_edit(id, db):
	# consumable data gets send to a form
	# nutrients are generated using ajax to keep track of removed
	modify_type = 'edit'

	# consumable types
	q = """SELECT * 
				FROM consumable_type"""
	c = db.execute(q)
	consumable_types = c.fetchall()

	# nutrients
	q = """SELECT * 
				FROM nutrient"""
	c = db.execute(q)
	nutrients = c.fetchall()

	# consumable info
	q = """SELECT c.id,
					c.title,
					c.calories,
					c.consumable_type_id  
				FROM consumable c 
				WHERE c.id = '{id}'""".format(id = id)
	c = db.execute(q)
	consumable = c.fetchone()
	# consumable has nutrients

	q = """SELECT n.id,
					n.title,
					chn.value  
			FROM consumable_has_nutrient chn 
				LEFT JOIN nutrient n ON (chn.nutrient_id = n.id)
			WHERE chn.consumable_id = '{id}'""".format(id = id)
	c = db.execute(q)
	consumable_nutrients = c.fetchall()
	consumable_nutrients = json.dumps([dict(x) for x in consumable_nutrients])
	return template('consumable.tpl', modify_type = modify_type, ct = consumable_types, n = nutrients, cn = consumable_nutrients, c = consumable)

@app.route('/consumable-enter')
def consumable_enter(db):
	# db manipulation gets through ajax
	# this is just to show template
	modify_type = 'enter'

	# consumable types
	q = """SELECT * 
				FROM consumable_type"""
	c = db.execute(q)
	consumable_types = c.fetchall()

	# nutrients
	q = """SELECT * 
				FROM nutrient"""
	c = db.execute(q)
	nutrients = c.fetchall()

	consumable_nutrients = None
	consumable = None

	return template('consumable.tpl', modify_type = modify_type, ct = consumable_types, n = nutrients, cn = consumable_nutrients, c = consumable)

# ajax crete
@app.route('/consumable-enter', method = 'POST')
def consumable_enter_post(db):

	try:
		req_json = request.json

		# 1. add consumable
		q = """INSERT INTO consumable 
					(title, consumable_type_id, calories)
					VALUES ( ?, ?, ? )"""

		c = db.execute(q, (req_json['title'], req_json['consumable_type_id'], req_json['calories']))

		if(c.rowcount > 0):

			# consumable id
			consumable_id = c.lastrowid

			# 2. add nutriens if exist
			if(req_json['nutrients'] and len(req_json['nutrients']) > 0):

				for nutrient in req_json['nutrients']:
					q = """INSERT INTO consumable_has_nutrient (consumable_id, nutrient_id, value) 
						VALUES (?, ?, ?)"""
					db.execute(q, (consumable_id, nutrient['id'], nutrient['value']))
				c = db.execute("COMMIT")
				return json.dumps("Consumable successfully created")
		
	except expression as identifier:
		abort(500, json.dumps(identifier))

@app.route('/nutrients')
def nutrients_list(db):

	q = """SELECT * 
				FROM nutrient n"""
	c = db.execute(q)
	nutrients = c.fetchall()

	# check if ajax or normal ( json / template )
	is_ajax = request.query.isAjax
	if is_ajax == '1':
		return json.dumps( [dict(ix) for ix in nutrients] )
	else:
		pass


debug(True)
run(app, host='localhost', port=8080, reloader=True)