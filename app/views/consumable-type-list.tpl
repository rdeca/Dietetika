%include('./base/header.tpl')
%include('./base/growl.tpl')
<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/consumable-types-enter'>Vnesi novega</a>
		<hr>
	</div>
	% if (len(consumable_types) != 0):
	<table class="table table-striped">
		<thead>
		  <tr>
			<th>Tip živila</th>
			<th></th>
			<th></th>
		  </tr>
		</thead>
		<tbody>
			% for c in consumable_types:
				<tr>
					<td style='width: 80%;'>
						<a href='/consumable-type/{{c["id"]}}'>
							{{c['title']}}
						</a>
					</td>

					<td class='manipulation-btns'>
						<a class='btn btn-info' href='/consumable-type-edit/{{c["id"]}}'>
							<span class="glyphicon glyphicon-pencil"></span> Uredi
						</a>
					</td>
					<td class='manipulation-btns'>
						<a class='btn btn-danger' href='/consumable-type-delete/{{c["id"]}}'>
							<span class="glyphicon glyphicon-trash"></span> Izbriši
						</a>
					</td>
				</tr>
			% end
		</tbody>
	  </table>
	  % else:
	  <p>Trenutno ni podatkov v bazi.</p>
	% end
</div>

%include('./base/footer.tpl')