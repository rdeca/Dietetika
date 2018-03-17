%include('./base/header.tpl')

<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/consumables'>Seznam vseh</a>
		<hr>
	</div>
	%include('./base/error.tpl')
	<div class="row">
		<div class="col-sm-8">
			<form id="consumable-modify" data-modify-type='{{modify_type}}'>
				% if (c and ('id' in c.keys())):
				<input id="consumable_id" type="text" value = '{{c["id"]}}' class='hidden'>
				% end

				<div class="form-group">
					<label for="title">Živilo:</label>
					<input type="text" class="form-control" id="title"
					% if (c and ('title' in c.keys())):
					value = '{{c["title"]}}'
					% end
					required data-required-error='Obvezno polje'>
					<div class="help-block with-errors alert alert-danger"></div>
				</div>
				<div class="form-group">
					<label for="consumable_type">Tip Živila:</label>
					<select name="consumable_type_select" id="consumable_type_select" required data-required-error='Izberite eno izmed izbir' class='form-control'>
						% for con_type in ct:
						<option value="{{con_type['id']}}" 
						% if (c and ('consumable_type_id' in c.keys()) and c['consumable_type_id'] == con_type['id']):
						selected
						% end
						 >{{con_type['title']}}</option>
						% end
					</select>
					<div class="help-block with-errors alert alert-danger"></div>
				</div>
				<div class="form-group">
					<label for="calories">Kalorije:</label>
					<input type="text" class="form-control" required data-required-error='Obvezno polje'id="calories" 
					% if (c and ('calories' in c.keys())):
					value='{{c["calories"]}}'
					% end
					>
					<div class="help-block with-errors alert alert-danger"></div>
				</div>
				<div class="form-group">
					<div id="consumable_nutrients_table_wrapper" class='hidden'>
						<label for="calories">Hranilne Vrednosti:</label>
						<table id="consumable_nutrients_table" class='table table-striped'
						% if (cn is not None):
							data-consumable-nutrients='{{cn}}'
						% end
						>
							<thead>
								<th>
									Tip
								</th>
								<th>
									g/100 g
								</th>
								<th>
									
								</th>
							</thead>
							<tbody>
								% #done with ajax on load
							</tbody>
						</table>
					</div>
					
					<br>
					<div class="form-group">
						<label for="add_nutrient" class='form-label'>Dodaj vrednost:</label>
						<div id='add-nutrient-to-consumable-wrapper'>
							<select name="nutrient" id="nutrient" class='form-control limit-width'>
								% for nutrient in n:
								<option value="{{nutrient['id']}}">{{nutrient['title']}}</option>
								% end
							</select>
							<input type="text" name="nutrient_value" id="nutrient_value" class='form-control limit-width smaller'>							<button type="button" id='add-nutrient-to-consumable' class='btn btn-primary'>
								<span class="glyphicon glyphicon-plus"></span> Add
							</button>
						</div>
					</div>
				</div>
				<button type="submit" class="btn btn-default">Shrani</button>
			</form>
		</div>
	</div>
</div>

%include('./base/footer.tpl')