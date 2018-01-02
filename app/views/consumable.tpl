%include('./base/header.tpl')

<div class="container main-content" data-modify-type='{{modify_type}}'>
	<div class="row">
		<div class="col-sm-8">
			<form action="/action_page.php">
				% if (c and c['id']):
				<input id="consumable_id" type="text" value = '{{c["id"]}}' class='hidden'>
				% end

				<div class="form-group">
					<label for="title">Consumable title:</label>
					<input type="text" class="form-control" id="title"
					% if (c['title']):
					value = '{{c["title"]}}'
					% end
					>
				</div>
				<div class="form-group">
					<label for="consumable_type">Consumable type:</label>
					<select name="consumable_type_select" id="consumable_type_select" class='form-control'>
						<option value="-1">Not selected</option>
						% for con_type in ct:
						<option value="{{con_type['id']}}" 
						% if (c is not None and c['consumable_type_id'] and c['consumable_type_id'] == con_type['id']):
						selected
						% end
						 >{{con_type['title']}}</option>
						% end
					</select>
				</div>
				<div class="form-group">
					<label for="calories">Calories:</label>
					<input type="text" class="form-control" id="calories" 
					% if (c['calories']):
					value='{{c["calories"]}}'
					% end
					>
				</div>
				<div class="form-group">
					<div id="consumable_nutrients_table_wrapper" class='hidden'>
						<label for="calories">Nutrients:</label>
						<table id="consumable_nutrients_table" class='table table-striped'
						% if (cn is not None):
							data-consumable-nutrients='{{cn}}'
						% end
						>
							<thead>
								<th>
									Nutrient
								</th>
								<th>
									Value
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
						<label for="add_nutrient" class='form-label'>Add nutrient:</label>
						<div id='add-nutrient-to-consumable-wrapper'>
							<select name="nutrient" id="nutrient" class='form-control limit-width'>
								<option value="-1">Not selected</option>
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
				<button type="submit" class="btn btn-default">Submit</button>
			</form>
		</div>
	</div>
</div>

%include('./base/footer.tpl')