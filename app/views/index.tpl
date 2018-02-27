
%include('./base/header.tpl')


<div class="container">
	<div id="entry-search" class="row">
		<div class="text-center">
			<h2>Poišči hranilo</h2>
		</div>
		<div class="col-xs-8 col-xs-offset-2">
			<form action="/consumables" method="GET">
				<input type="text" name="title" class="form-control">
				<div class="text-center">
					<button type="submit" class="btn btn-primary">
						<i class="glyphicon glyphicon-search"></i>	Najdi
					</button>
				</div>
			</form>
		</div>
	</div>
</div>




%include('./base/footer.tpl')