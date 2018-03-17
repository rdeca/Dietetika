import bottle
import bottle.ext.sqlite
from bottle import Bottle, abort, response, run, static_file, template, debug, redirect, request
import json
import sys

app = Bottle()

#install db connection
plugin = bottle.ext.sqlite.Plugin(dbfile='./db/dietetika.sqlite')
app.install(plugin)

app.catchall = False


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
	return template('index.tpl')

@app.route('/entry')
def domov():
	redirect('/')
    
# prikaz zivil
@app.route('/consumables')
def consumables(db):

	is_ajax = request.query.isAjax # komunicira s strežnikom, ne rabimo refreshat

	if is_ajax == '1': #če je ena vrne podatek autocomplete
		query = request.query.query #kar smo napisali v okno

		q = """SELECT id, title 
				FROM consumable 
				WHERE title LIKE :title"""

		title_string = "%{title}%".format(title = query)
		c = db.execute(q, {'title': title_string})
		results = c.fetchall()

		results_dict = [x['title'] for x in results] #json prebere

		returned_dict = {'suggestions': results_dict}

		return json.dumps(returned_dict)
	else: #vrne stran
		#uporaben ko so posredovani search parameteri
		query_dict = {}

		title = request.query.title
		consumable_type_id = request.query.consumable_type_select

		q = """SELECT c.id,
					c.title,
					c.calories,
					ct.title as consumable_type_title,
					count(chn.nutrient_id) as nutrient_count 
			FROM consumable c 
				LEFT JOIN consumable_type ct ON (c.consumable_type_id = ct.id) 
				LEFT JOIN consumable_has_nutrient chn ON (chn.consumable_id = c.id) 
			WHERE 1 """

		if title: #če smo kej zapisali v search
			title_string = "%{title}%".format(title=title)
			query_dict['title'] = title_string
			q += " AND c.title LIKE :title "
		if consumable_type_id: #iščemo tip
			query_dict['consumable_type_id'] = consumable_type_id
			q += " AND c.consumable_type_id = :consumable_type_id "

		q += """GROUP BY c.id
			ORDER BY c.id"""

		c = db.execute(q, query_dict)
		r_consumables = c.fetchall()

		q = """SELECT * FROM consumable_type"""
		c = db.execute(q)
		consumable_types = c.fetchall()

		return template("consumables-list.tpl", consumables = r_consumables, consumable_types = consumable_types, status_text = None)


# prikaz podatkov o zivilu
@app.route('/consumable/<consumable_id>') #<> obvezen parameter
def consumable(consumable_id, db):
	q = """SELECT c.id, 
					c.title,
					ct.title as consumable_type_title,
					c.calories 
				FROM consumable c 
				LEFT JOIN consumable_type ct ON (c.consumable_type_id = ct.id) 
				WHERE c.id = ?"""
	c = db.execute(q, (consumable_id,))
	consumable = c.fetchone()
	q_nutrients = """SELECT n.id,
							n.title,
							nt.title as nutrient_type_title,
							chn.value  
						FROM consumable_has_nutrient chn 
							LEFT JOIN nutrient n ON (chn.nutrient_id = n.id)
							LEFT JOIN nutrient_type nt ON (n.nutrient_type_id = nt.id)
						WHERE chn.consumable_id = ? """
	c = db.execute(q_nutrients, (consumable_id,))
	nutrients = c.fetchall()
	return template("consumable-details.tpl", c = consumable, n = nutrients)

# brisanje zivila
@app.route('/consumable-delete/<id>')
def consumable_delete(id, db):
	q = "DELETE FROM consumable WHERE id = ? "
	c = db.execute(q,(id,))
	if c.rowcount == 1: #koliko vrstic se je spremenilo
		redirect('/consumables?changes=deleted')
	else:
		redirect('/consumable/{id}'.format(id=id))


# prikaz podatkov za urejanje zivila
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
				WHERE c.id = ? """
	c = db.execute(q, (id,))
	consumable = c.fetchone()
	# consumable has nutrients

	q = """SELECT n.id,
					n.title,
					chn.value  
			FROM consumable_has_nutrient chn 
				LEFT JOIN nutrient n ON (chn.nutrient_id = n.id)
			WHERE chn.consumable_id = ? """
	c = db.execute(q, (id,))
	consumable_nutrients = c.fetchall()
	consumable_nutrients = json.dumps([dict(x) for x in consumable_nutrients])
	return template('consumable.tpl', modify_type = modify_type, ct = consumable_types, n = nutrients, cn = consumable_nutrients, c = consumable, e = None)

# shranjevanje v bazo urejanje zivila
# ajax in json
@app.route('/consumable-edit/<id>', method='POST')
def consumable_edit(id, db):
	try:
		db.isolation_level = "DEFERRED"
		req_json = request.json

		q = """UPDATE consumable 
				SET title = ?, 
				consumable_type_id = ?, 
				calories = ? 
			WHERE id = ?"""
		
		db.execute(q, (req_json['title'], req_json['consumable_type_id'], req_json['calories'], id))

		valid_nutrient_ids = []
		for nutrient in req_json['nutrients']:
			# 1.check if combination exists in this case change value
			q = """SELECT * FROM consumable_has_nutrient WHERE consumable_id = ? AND nutrient_id = ?; """
			c = db.execute(q, (id, nutrient['id']))
			consumable_nutrient = c.fetchone()

			valid_nutrient_ids.append(nutrient['id'])

			if (consumable_nutrient is not None):
				q = """UPDATE consumable_has_nutrient SET value = ? WHERE consumable_id = ? AND nutrient_id = ?;"""
				db.execute(q, (nutrient['value'], id, nutrient['id']))
			else: 
				q = """INSERT INTO consumable_has_nutrient (consumable_id, nutrient_id, value) VALUES (?, ?, ?);"""
				db.execute(q, (id, nutrient['id'], nutrient['value']))
			
		# 2. delete those that dont fix
		
		# valid_nutrient_ids = '(' + valid_nutrient_ids + ')'
		q = """DELETE FROM consumable_has_nutrient WHERE consumable_id = ? AND nutrient_id NOT IN (%s)""" % ("?," * len(valid_nutrient_ids))[:-1]
		valid_nutrient_ids.insert(0, id)
		c = db.execute(q, valid_nutrient_ids)
		return json.dumps('Živilo uspešno posodobljeno.')
	except db.IntegrityError:
		response.status = 500
		return 'Živilo s takšnim imenom že obstaja'
	except db.Error:
		e = sys.exc_info()[0]
		db.rollback()
		response.status = 500
		return e
	except:
		e = sys.exc_info()[0]
		response.status = 500
		return e

#prikaz vnosnih polj za vnos zivila
@app.route('/consumables-enter')
def consumable_enter(db):
	# db manipulation gets through ajax
	# this is just to show template
	modify_type = 'enter' #zapis v html je data- modity_type za enter in edit je isti template

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

	consumable_nutrients = None #tuki še ne obstaja
	consumable = None

	return template('consumable.tpl', modify_type = modify_type, ct = consumable_types, n = nutrients, cn = consumable_nutrients, c = consumable, e = None)

# ajax create za vnos zivila
@app.route('/consumables-enter', method = 'POST')
def consumable_enter_post(db): #dietetika js

	try:
		db.isolation_level = "DEFERRED"
		req_json = request.json

		# 1. add consumable
		q = """INSERT INTO consumable 
					(title, consumable_type_id, calories)
					VALUES ( ?, ?, ? )"""

		c = db.execute(q, (req_json['title'], req_json['consumable_type_id'], req_json['calories']))

		if(c.rowcount > 0):

			# consumable id
			consumable_id = c.lastrowid #zadnji vnešeni

			# 2. add nutriens if exist
			if(req_json['nutrients'] and len(req_json['nutrients']) > 0):

				for nutrient in req_json['nutrients']:
					q = """INSERT INTO consumable_has_nutrient (consumable_id, nutrient_id, value) 
						VALUES (?, ?, ?)"""
					db.execute(q, (consumable_id, nutrient['id'], nutrient['value']))
				c = db.commit()
				return json.dumps("Živilo uspešno ustvarjeno.")
	except db.IntegrityError:
		db.rollback()
		response.status = 500
		return "Živilo s takšnim imenom že obstaja"
	except db.Error:
		e = sys.exc_info()[0]
		db.rollback() #skensli vse kar je do zdej vnešeno
		response.status = 500 #napaka na serverju
		return e #console error
	except:
		e = sys.exc_info()[0]
		response.status = 500
		return e

# prikaz hranil
@app.route('/nutrients')
def nutrients_list(db):

	# check if ajax or normal ( json / template )
	is_ajax = request.query.isAjax
	if is_ajax == '1':	
		q = """SELECT * 
					FROM nutrient n"""
		c = db.execute(q)
		nutrients = c.fetchall()
		return json.dumps( [dict(ix) for ix in nutrients] )
	else: 
		q = """SELECT n.id,
						n.title,
						nt.title as nutrient_type_title 
					FROM nutrient n 
						LEFT JOIN nutrient_type nt ON (n.nutrient_type_id = nt.id)"""
		c = db.execute(q)
		nutrients = c.fetchall()
		return template('nutrient-list.tpl', nutrients = nutrients)

#prikaz podatkov o hranilu
@app.route('/nutrient/<id>')
def nutrient_details(id, db):
	q = """SELECT n.id,
					n.title,
					nt.id as nutrient_type_id,
					nt.title as nutrient_type_title
				FROM nutrient n 
					LEFT JOIN nutrient_type nt ON (n.nutrient_type_id = nt.id) 
				WHERE n.id = ?"""
	
	c = db.execute(q, (id,))
	nutrient = c.fetchone()

	return template('nutrient-details.tpl', n = nutrient)

# brisanje hranila
@app.route('/nutrient-delete/<id>')
def nutrient_delete(id, db):
	q = """DELETE FROM nutrient WHERE id = ?"""
	db.execute(q, (id,))
	redirect('/nutrients?changes=deleted')

# prikaz vnostnih polj pri vnosu hranila
@app.route('/nutrients-enter')
def nutrient_enter(db):

	q = """SELECT * FROM nutrient_type;""" #pokažemo v dropdownu
	c = db.execute(q)
	nutrient_types = c.fetchall()

	return template('nutrient.tpl', nt = nutrient_types, n = None, e = None)

# shranjevanje podatkov v bazo pri vnosu novega hranila
@app.route('/nutrients-enter', method='POST') #isto kot app.post je na isti strani
def nutrient_enter_post(db):
	try:
		title = request.forms.title #glede na name
		#ker je INT FK ga je potrebno pretvorit iz stringa v int, drugače ne primerja prov v integrity err templateu
		nutrient_type_id = int(request.forms.nutrient_type_id) 
		nutrient = {'title': title, 'nutrient_type_id': nutrient_type_id}
		q = """INSERT INTO nutrient (title, nutrient_type_id) VALUES (:title, :nutrient_type_id);"""
		c = db.execute(q, nutrient)
		if (c.rowcount > 0):
			redirect('/nutrients?changes=saved')
	except db.IntegrityError:
		q = """SELECT * FROM nutrient_type;""" #pokažemo v dropdownu
		c = db.execute(q)
		nutrient_types = c.fetchall()
		return template('nutrient.tpl', nt = nutrient_types, n = nutrient, e = "Hranilo s takšnim imenom že obstaja")


# prikaz podatkov pri urejanju hranila
@app.route('/nutrient-edit/<id>')
def nutrient_edit(id, db): #id rabimo da iščemo v bazi

	#nutrient details
	q = """SELECT * FROM nutrient WHERE id = ?; """
	c = db.execute(q, (id,))
	nutrient = c.fetchone()

	#nutrient types
	q = """SELECT * FROM nutrient_type;"""
	c = db.execute(q)
	nutrient_types = c.fetchall()

	return template('nutrient.tpl', n = nutrient, nt = nutrient_types, e = None)

# shranjevanje v bazo pri urejanju hranila
@app.route('/nutrient-edit/<id>', method='POST')
def nutrient_edit_post(id, db):

	try: 
		title = request.forms.title
		nutrient_type_id = int(request.forms.nutrient_type_id) #string v int ( ni potrebno za bazo ampak ce pride do integrity err in b)
		nutrient = {'title': title, 'nutrient_type_id': nutrient_type_id, 'id': id}
		q = """UPDATE nutrient SET title = :title, nutrient_type_id = :nutrient_type_id WHERE id = :id;"""
		c = db.execute(q, nutrient)

		if (c.rowcount > 0):
			redirect('/nutrients?changes=updated')
	except db.IntegrityError:
		q = """SELECT * FROM nutrient_type;""" #pokažemo v dropdownu
		c = db.execute(q)
		nutrient_types = c.fetchall()
		return template('nutrient.tpl', n = nutrient, nt = nutrient_types, e = 'Hranilo s takim imenom že obstaja')

#tipi zivil
@app.route('/consumable-types')
def consumable_types(db):
	q = """SELECT * FROM consumable_type"""
	c = db.execute(q)

	consumable_types = c.fetchall()
	
	return template('consumable-type-list.tpl', consumable_types = consumable_types)

#brisanje tipa zivila
@app.route('/consumable-type-delete/<id>')
def consumable_types_delete(id, db):
	q = """DELETE FROM consumable_type WHERE id =:id;"""
	c = db.execute(q, {'id': id})

	if (c.rowcount > 0):
		redirect('/consumable-types?changes=deleted')

#prikaz tipov zivila
@app.route('/consumable-type/<id>')
def consumable_types_details(id, db):
	q = """SELECT * FROM consumable_type WHERE id = ?;"""
	c = db.execute(q, (id,))
	
	consumable_type = c.fetchone()
	return template('consumable-types-details.tpl', ct = consumable_type)	

#prikaz podatkov za urejanje tipa zivila
@app.route('/consumable-type-edit/<id>')
def consumable_types_edit(id, db):
	q = """SELECT * FROM consumable_type WHERE id = :id;"""
	c = db.execute(q, {'id': id})
	consumable_type = c.fetchone()

	return template('consumable-types.tpl', ct = consumable_type, e = None)

#shranjevanje sprememb pri urejanju tipa zivila
@app.route('/consumable-type-edit/<id>', method='POST')
def consumable_types_edit_post(id, db):
	try:
		title = request.forms.title
		consumable_type = {'title': title, 'id': id}
		q = """UPDATE consumable_type SET title = :title WHERE id = :id;"""
		c = db.execute(q, consumable_type)
		if (c.rowcount > 0):
			redirect('/consumable-types?changes=updated')
	except db.IntegrityError as e:
			return template('consumable-types.tpl', ct = consumable_type, e = "Tip živila s takim imenom že obstaja")

#prikaz vnosnih polj za vnos tipa zivila
@app.route('/consumable-types-enter')
def consumable_types_enter(db):
	return template('consumable-types.tpl', ct = None, e = None)

#shranjevanje v bazo novega tipa zivila
@app.route('/consumable-types-enter', method='POST')
def consumable_types_enter_post(db):
	try:
		consumable_type_title = request.forms.title
		consumable_type = {'title': consumable_type_title}
		q = """INSERT INTO consumable_type (title) VALUES (:title);"""
		c = db.execute(q, consumable_type)

		if (c.rowcount > 0):
			redirect('/consumable-types?changes=created')
	except db.IntegrityError as e:
		return template('consumable-types.tpl', ct = consumable_type, e = "Tip živila s takim imenom že obstaja")

#prikaz tipov hranila
@app.route('/nutrient-types')
def nutrient_types(db):
	q = "SELECT * FROM nutrient_type;"
	c = db.execute(q)
	nutrient_types = c.fetchall()
	return template('nutrient-type-list.tpl', nutrient_types = nutrient_types)

#moznost novega vnosa tipa hranila
@app.route('/nutrient-types-enter')
def nutrient_types_enter(db):
	return template('nutrient-type.tpl', nt = None, e = None)

#shranjevanje v bazo tipa hranila
@app.route('/nutrient-types-enter', method='POST')
def nutrient_types_enter_post(db):
	try:
		title = request.forms.title
		q = """INSERT INTO nutrient_type (title) VALUES (:title);"""
		nutrient_type = {'title': title}
		c = db.execute(q, nutrient_type)
		if (c.rowcount > 0):
			redirect('/nutrient-types?changes=created')
	except db.IntegrityError:
		return template('nutrient-type.tpl', nt = nutrient_type, e = "Tip hranila s takim imenom že obstaja")

#prikaz podatkov pri urejanju tipa hranila
@app.route('/nutrient-type-edit/<id>')
def nutrient_types_edit(id, db):
	q = "SELECT * FROM nutrient_type WHERE id=:id;"
	c = db.execute(q, {'id': id})
	nutrient_type = c.fetchone()
	return template('nutrient-type.tpl', nt = nutrient_type, e = None)

#shrani spremembe pri urejanju tupa hranila
@app.route('/nutrient-type-edit/<id>', method = 'POST')
def nutrient_types_edit_post(id, db):
	try:
		title = request.forms.title
		nutrient_type = {'title': title, 'id':id}
		q = """UPDATE nutrient_type SET title=:title WHERE id=:id;"""
		c = db.execute(q, nutrient_type)
		if (c.rowcount>0):
			redirect('/nutrient-types?changes=updated')
	except db.IntegrityError:
		return template('nutrient-type.tpl', nt = nutrient_type, e = "Tip hranila s takim imenom že obstaja")

#prikaze tip hranila
@app.route('/nutrient-type/<id>')
def nutrient_type(id, db):
	q = "SELECT * FROM nutrient_type WHERE id=:id;"
	c = db.execute(q, {'id': id})
	nutrient_type = c.fetchone()
	return template('nutrient-type-details.tpl', nt = nutrient_type)

#izbrise tip hranila
@app.route('/nutrient-type-delete/<id>')
def nutrient_type_delete(id, db):
	q = "DELETE FROM nutrient_type WHERE id=:id;"
	c = db.execute(q, {'id': id})
	if (c.rowcount > 0):
		redirect('/nutrient-types?changes=deleted')

debug(True) #piše errorje
run(app, host='localhost', port=8080, reloader=True)
