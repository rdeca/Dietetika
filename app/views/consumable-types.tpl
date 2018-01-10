%include('./base/header.tpl')

<div class="container main-content">
	<div id="errors-wrapper" class="alert alert-danger hidden">
		<ul>

		</ul>
	</div>
	<div class="row">
		<div class="col-sm-8">
			<form id="nutrient-modify" method='POST'>
				% if (ct and ct['id']):
				<input id="name" type="text" name='id' value = '{{ct["id"]}}' class='hidden'>
				% end

				<div class="form-group">
					<label for="title">Consumable type:</label>
					<input name="title" type="text" required data-required-error='Obvezno polje' pattern='[\w-]+'data-pattern-error='Neveljavni znaki v polju'  class="form-control" id="title"
					% if (ct and ct['title']):
					value = '{{ct["title"]}}'
					% end
					>
					<div class="help-block with-errors alert alert-danger"></div>
				</div>
				<button type="submit" class="btn btn-default">Submit</button>
			</form>
		</div>
	</div>
</div>

%include('./base/footer.tpl')