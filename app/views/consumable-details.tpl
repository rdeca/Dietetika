
%include('./base/header.tpl')

<div class="container main-content">
	% if c:
		<dl>
			<dt>Title</dt>
			<dd>{{c['title']}}</dd>
			<dt>Consumable type</dt>
			<dd>{{c['consumable_type_title']}}</dd>
			<dt>Consumable type parent</dt>
			<dd>{{c['consumable_type_parent_title']}}</dd>
			<dt>Consumable type parent</dt>
			<dd>{{c['calories']}}</dd>
			% if len(n) > 0:
			<dt>Nurients</dt>
			<dd>
				<ul>
					% for nutrient in n:
					<li>
						<dl>
							<dt>
								Nutrient title
							</dt>
							<dd>
								{{nutrient['title']}}
							</dd>
							<dt>
								Nutrient parent
							</dt>
							<dd>
								{{nutrient['nutrient_type_title']}}
							</dd>
							<dt>
								Nutrient value
							</dt>
							<dd>
								{{nutrient['value']}}
							</dd>
						</dl>
						
					</li>
					% end 
				</ul>
			</dd>
			% end
		</dl>
		<div class="clearfix"></div>
		<div class="entry-manipulation">
			<a href="/consumable-edit/{{c['id']}}" class="btn btn-primary">
				<span class='glyphicon glyphicon-pencil'></span>Edit
			</a>
			<a href="/consumable-delete/{{c['id']}}" class="btn btn-danger">
				<span class='glyphicon glyphicon-remove'></span>Delete
			</a>
		</div>
	% else:
	<p>Ni vnosa za izbran id.</p>
	% end
</div>

%include('./base/footer.tpl')