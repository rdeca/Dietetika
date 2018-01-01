
def random_entry_fk (fk_range):
	#returns random 'fk' in range

	#starts with 1 because unsigned id
	return random.randint(1, fk_range-1) #because it includes boundaries and range doesnt 

def generate_sql_file():

	# VARS
	# ----------------------------------------------

	#outputfile
	outputfile_name = 'dietetika-generate.sql'

	# num of entries
	nutrinet_types_num = 5
	nutrients_num = 10
	consumable_type_parent_num = 3
	consumable_types_num = 10
	consumables_num = 100

	#base names
	nutrient_type_name = 'nutrient type entry '
	nutrient_name = 'nutrient '
	consumable_type_parent_name = 'consumable type parent '
	consumable_types_name = 'consumable type '
	consumables_name = 'consumable'

	#calories
	calories_base = [10, 100, 1000, 10000]

	# calories has nutrients 
	max_num_of_nutrients_per_consumable = 5
	nutrients_value_base = [10, 100, 1000, 10000]

	sqlscript = ''


	# SQL CODE ITERATIONS
	# ----------------------------
	
	#nutrient type
	for i in range(1,nutrinet_types_num):
		s = Template('INSERT INTO nutrient_type (id, title) VALUES ($id, "$title");')
		sql_insert = s.substitute(id = i, title = nutrient_type_name + str(i))
		sqlscript += sql_insert

	#nutrient
	for i in range(1,nutrients_num):
		s = Template('INSERT INTO nutrient (id, title, nutrient_type_id) VALUES ($id, "$title", $nutrient_type_id);')
		nutrient_type_id = random_entry_fk(nutrinet_types_num)
		sql_insert = s.substitute(id = i, title = nutrient_name + str(i), nutrient_type_id = str(nutrient_type_id))
		sqlscript += sql_insert

	#consumable type parent
	for i in range(1, consumable_type_parent_num):
		s = Template('INSERT INTO consumable_type_parent (id, title) VALUES ($id, "$title");')
		sql_insert = s.substitute(id = i, title = consumable_type_parent_name + str(i))
		sqlscript += sql_insert

	#consumable type
	for i in range(1, consumable_types_num):
		s = Template('INSERT INTO consumable_type (id, title, consumable_type_parent_id) VALUES ($id, "$title", $consumable_type_parent_id);')
		consum_parent_type_id = random_entry_fk(consumable_type_parent_num)
		sql_insert = s.substitute(id = i, title = consumable_types_name + str(i), consumable_type_parent_id = consum_parent_type_id)
		sqlscript += sql_insert

	#consumable
	for i in range(1, consumables_num):
		s = Template('INSERT INTO consumable (id, title, calories, consumable_type_id) VALUES ($id, "$title", $calories, $consumable_type_id);')
		calories_num = round(random.random() * calories_base[random.randint(0, len(calories_base)-1)], 2)
		consum_type_id = random_entry_fk(consumable_types_num)
		sql_insert = s.substitute(id = i, title = consumables_name + str(i), calories = calories_num, consumable_type_id = consum_type_id)
		sqlscript += sql_insert

	#consumalbe has nutrient
	#this could be appended to previous iteration but for better visibiltiy its here ( and because not mil of entries)
	for consumable in range(1, consumables_num):
		s = Template('INSERT INTO consumable_has_nutrient (nutrient_id, consumable_id, value) VALUES ($nutrient_id, $consumable_id, $value);')
		
		#consumable has random num of nutrients
		rand_num_of_nutrients = random.randint(1, max_num_of_nutrients_per_consumable)
		inserted_nutrients = []
		for cons_nutrient in range(0, rand_num_of_nutrients):
			nutrients_val = round(random.random() * nutrients_value_base[random.randint(0, len(nutrients_value_base)-1)], 2)
			cons_nutrient_type_id = random_entry_fk(nutrients_num)
			while True:
				#because we cant insert a nutrint we already inserted for a consumable
				if(cons_nutrient_type_id not in inserted_nutrients):
					inserted_nutrients.append(cons_nutrient_type_id)
					break
				else:
					# get new nutrient id because last one was already inserted
					cons_nutrient_type_id = random_entry_fk(nutrients_num)
			sql_insert = s.substitute(nutrient_id = cons_nutrient_type_id, consumable_id = consumable, value = nutrients_val)
			sqlscript += sql_insert


	#write to sql file
	f = open(outputfile_name, 'w')
	f.write(sqlscript)
	f.close()

	print('{0} successfully generated.'.format(outputfile_name))


if __name__ == '__main__':
	from string import Template
	import random
	print(generate_sql_file())