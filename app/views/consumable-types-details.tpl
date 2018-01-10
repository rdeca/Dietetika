
%include('./base/header.tpl')

<div class="container main-content">
	% if ct:
		<dl>
			<dt>Title</dt>
			<dd>{{ct['title']}}</dd>
		</dl>
		<div class="clearfix"></div>
		<div class="entry-manipulation">
			<a href="/consumable-types-edit/{{ct['id']}}" class="btn btn-primary">
				<span class='glyphicon glyphicon-pencil'></span>Edit
			</a>
			<a href="/consumable-types-delete/{{ct['id']}}" class="btn btn-danger">
				<span class='glyphicon glyphicon-remove'></span>Delete
			</a>
		</div>
	% else:
	<p>Ni vnosa za izbran id.</p>
	% end
</div>

%include('./base/footer.tpl')