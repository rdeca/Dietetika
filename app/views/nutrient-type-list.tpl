%include('./base/header.tpl')

<div class="container main-content">
	% if (len(nutrient_types) != 0):
	<table class="table table-striped">
		<thead>
		  <tr>
			<th>Nutrient type</th>
			<th></th>
			<th></th>
		  </tr>
		</thead>
		<tbody>
			% for nt in nutrient_types:
				<tr>
					<td style='width: 50%;'>
						<a href='/nutrient-types/{{nt["id"]}}'>
							{{nt['title']}}
						</a>
					</td>
					<td style='width: 50%;'>
						{{nt['title']}}
					</td>
					<td class='manipulation-btns'>
						<a class='btn btn-info' href='/nutrient-types-edit/{{nt["id"]}}'>
							<span class="glyphicon glyphicon-pencil"></span> Edit
						</a>
					</td>
					<td class='manipulation-btns'>
						<a class='btn btn-danger' href='/nutrient-types-delete/{{nt["id"]}}'>
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