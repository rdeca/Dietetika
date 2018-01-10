%include('./base/header.tpl')

<div class="container main-content">
	% if (len(consumable_types) != 0):
	<table class="table table-striped">
		<thead>
		  <tr>
			<th>Consumable type</th>
			<th></th>
			<th></th>
		  </tr>
		</thead>
		<tbody>
			% for c in consumable_types:
				<tr>
					<td style='width: 50%;'>
						<a href='/consumable-types/{{c["id"]}}'>
							{{c['title']}}
						</a>
					</td>
					<td style='width: 50%;'>
						{{c['title']}}
					</td>
					<td class='manipulation-btns'>
						<a class='btn btn-info' href='/consumable-types-edit/{{c["id"]}}'>
							<span class="glyphicon glyphicon-pencil"></span> Edit
						</a>
					</td>
					<td class='manipulation-btns'>
						<a class='btn btn-danger' href='/consumable-types-delete/{{c["id"]}}'>
							<span class="glyphicon glyphicon-trash"></span> Delete
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