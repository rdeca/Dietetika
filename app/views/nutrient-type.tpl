%include('./base/header.tpl')

<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/nutrient-types'>Seznam vseh</a>
		<hr>
	</div>
	%include('./base/error.tpl')
	<div class="row">
		<div class="col-sm-8">
			<form id="nutrient-modify" method='POST'>
				% if (nt and ('id' in nt.keys())):
				<input id="name" type="text" name='id' value = '{{nt["id"]}}' class='hidden'>
				% end

				<div class="form-group">
					<label for="title">Tip:</label>
					<input name="title" type="text" required data-required-error='Obvezno polje' class="form-control" id="title"
					% if (nt and ('title' in nt.keys())):
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