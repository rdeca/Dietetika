
%include('./base/header.tpl')

<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/consumable-types'>Seznam vseh</a>
		<hr>
	</div>
	% if ct:
		<dl>
			<dt>Tip</dt>
			<dd>{{ct['title']}}</dd>
		</dl>
		<div class="clearfix"></div>
		<div class="entry-manipulation">
			<a href="/consumable-type-edit/{{ct['id']}}" class="btn btn-primary">
				<span class='glyphicon glyphicon-pencil'></span>Uredi
			</a>
			<a href="/consumable-type-delete/{{ct['id']}}" class="btn btn-danger">
				<span class='glyphicon glyphicon-remove'></span>Izbriši
			</a>
		</div>
	% else:
	<p>Ni vnosa za izbran id.</p>
	% end
</div>

%include('./base/footer.tpl')