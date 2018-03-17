%include('./base/header.tpl')

<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/nutrients'>Seznam vseh</a>
		<hr>
	</div>
	%include('./base/error.tpl')
	<div class="row">
		<div class="col-sm-8">
			<form id="nutrient-modify" method='POST'>
				% if (n and ('id' in n.keys())):
				<input type="text" name='id' value = '{{n["id"]}}' class='hidden'>
				% end

				<div class="form-group">
					<label for="title">Hranilo:</label>
					<input name="title" type="text" class="form-control" id="title"
					% if (n and ('title' in n.keys())):
					value = '{{n["title"]}}'
					% end
					required data-required-error='Obvezno polje'>
					<div class="help-block with-errors alert alert-danger"></div>

				</div>
				<div class="form-group">
					<label for="nutrient_type">Tip:</label>
					<select name="nutrient_type_id" data-required data-required-error='Izberite eno izmed izbir' id="nutrient_type_id" class='form-control'>
						% for nut_type in nt:
						<option value="{{nut_type['id']}}" 
						% if (n and ('nutrient_type_id' in n.keys()) and n['nutrient_type_id'] == nut_type['id']):
						selected
						% end
						 >{{nut_type['title']}}</option>
						% end
					</select>
					<div class="help-block with-errors alert alert-danger"></div>

				</div>
				<button type="submit" class="btn btn-default">Shrani</button>
			</form>
		</div>
	</div>
</div>

%include('./base/footer.tpl')