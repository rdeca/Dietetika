
%include('./base/header.tpl')

<div class="container main-content">
	% if n:
		<dl>
			<dt>Title</dt>
			<dd>{{n['title']}}</dd>
			<dt>Nutrient type</dt>
			<dd>{{n['nutrient_type_title']}}</dd>
		</dl>
		<div class="clearfix"></div>
		<div class="entry-manipulation">
			<a href="/nutrient-edit/{{n['id']}}" class="btn btn-primary">
				<span class='glyphicon glyphicon-pencil'></span>Edit
			</a>
			<a href="/nutrient-delete/{{n['id']}}" class="btn btn-danger">
				<span class='glyphicon glyphicon-remove'></span>Delete
			</a>
		</div>
	% else:
	<p>Ni vnosa za izbran id.</p>
	% end
</div>

%include('./base/footer.tpl')