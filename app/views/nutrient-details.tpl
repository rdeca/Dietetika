
%include('./base/header.tpl')

<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/nutrients'>Seznam vseh</a>
		<hr>
	</div>
	% if n:
		<dl>
			<dt>Hranilo</dt>
			<dd>{{n['title']}}</dd>
			<dt>Mikro/Makro</dt>
			<dd>{{n['nutrient_type_title']}}</dd>
		</dl>
		<div class="clearfix"></div>
		<div class="entry-manipulation">
			<a href="/nutrient-edit/{{n['id']}}" class="btn btn-primary">
				<span class='glyphicon glyphicon-pencil'></span>Uredi
			</a>
			<a href="/nutrient-delete/{{n['id']}}" class="btn btn-danger">
				<span class='glyphicon glyphicon-remove'></span>Izbriši
			</a>
		</div>
	% else:
	<p>Ni vnosa za izbran id.</p>
	% end
</div>

%include('./base/footer.tpl')