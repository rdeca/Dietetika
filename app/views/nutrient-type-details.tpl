
%include('./base/header.tpl')

<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/nutrient-types'>Seznam vseh</a>
		<hr>
	</div>
	% if nt:
		<dl>
			<dt>Title</dt>
			<dd>{{nt['title']}}</dd>
		</dl>
		<div class="clearfix"></div>
		<div class="entry-manipulation">
			<a href="/nutrient-type-edit/{{nt['id']}}" class="btn btn-primary">
				<span class='glyphicon glyphicon-pencil'></span>Edit
			</a>
			<a href="/nutrient-type-delete/{{nt['id']}}" class="btn btn-danger">
				<span class='glyphicon glyphicon-remove'></span>Delete
			</a>
		</div>
	% else:
	<p>Ni vnosa za izbran id.</p>
	% end
</div>

%include('./base/footer.tpl')