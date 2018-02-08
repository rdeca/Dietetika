%include('./base/header.tpl')

<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/nutrient-types'>Seznam vseh</a>
		<hr>
	</div>
	<div id="errors-wrapper" class="alert alert-danger hidden">
		<ul>

		</ul>
	</div>
	<div class="row">
		<div class="col-sm-8">
			<form id="nutrient-modify" method='POST'>
				% if (nt and nt['id']):
				<input id="name" type="text" name='id' value = '{{nt["id"]}}' class='hidden'>
				% end

				<div class="form-group">
					<label for="title">Tip:</label>
					<input name="title" type="text" required data-required-error='Obvezno polje' class="form-control" id="title"
					% if (nt and nt['title']):
					value = '{{nt["title"]}}'
					% end
					>
					<div class="alert alert-danger help-block with-errors"></div>
				</div>
				<button type="submit" class="btn btn-default">Shrani</button>
			</form>
		</div>
	</div>
</div>

%include('./base/footer.tpl')