%include('./base/header.tpl')
%include('./base/growl.tpl')
<div class="container main-content">
	<div class="anchors text-right">
		<a class='btn btn-primary' href='/nutrients-enter'>Vnesi novega</a>
		<hr>
	</div>
	% if (len(nutrients) != 0):
	<table class="table table-striped">
		<thead>
		  <tr>
			<th>Hranilo</th>
			<th>Tip Hranila</th>
			<th></th>
			<th></th>
		  </tr>
		</thead>
		<tbody>
			% for n in nutrients:
				<tr>
					<td style='width: 50%;'>
						<a href='/nutrient/{{n["id"]}}'>
							{{n['title']}}
						</a>
					</td>
					<td style='width: 50%;'>
						{{n['nutrient_type_title']}}
					</td>
					<td class='manipulation-btns'>
						<a class='btn btn-info' href='/nutrient-edit/{{n["id"]}}'>
							<span class="glyphicon glyphicon-pencil"></span> Uredi
						</a>
					</td>
					<td class='manipulation-btns'>
						<a class='btn btn-danger' href='/nutrient-delete/{{n["id"]}}'>
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