
%include('./base/header.tpl')

<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/consumables'>Seznam vseh</a>
		<hr>
	</div>
	% if c:
		<dl>
			<dt>Živilo</dt> 
			<dd>{{c['title']}}</dd>
			<dt>Tip živila</dt>
			<dd>{{c['consumable_type_title']}}</dd>
			<dt>Število kalorij na 100 g</dt>
			<dd>{{c['calories']}}</dd>
			% if len(n) > 0:
			<dt>Hranilne vrednosti </dt>
			<dd>
				<ul>
					% for nutrient in n:
					<li>
						<dl>
							<dt>
								{{nutrient['title']}}
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
				<span class='glyphicon glyphicon-pencil'></span>Uredi
			</a>
			<a href="/consumable-delete/{{c['id']}}" class="btn btn-danger">
				<span class='glyphicon glyphicon-remove'></span>Izbriši
			</a>
		</div>
	% else:
	<p>Ni vnosa za izbran id.</p>
	% end
</div>

%include('./base/footer.tpl')