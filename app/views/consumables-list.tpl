%include('./base/header.tpl')

<div class="container">
	% if (len(consumables) != 0):
	<table class="table table-striped">
		<thead>
		  <tr>
			<th>Consumable</th>
			<th>Consumable type</th>
			<th>Consumable type parent</th>
			<th>Calories</th>
			<th>Nutrients</th>
		  </tr>
		</thead>
		<tbody>
			% for c in consumables:
				<tr>
					<td>
						{{c['title']}}
					</td>
					<td>
						{{c['consumable_type_title']}}
					</td>
					<td>
						{{c['consumable_type_parent_title']}}
					</td>
					<td>
						{{c['calories']}}
					</td>
					<td>

						% if int(c['nutrient_count']) > 0:
							<a href='/consumable/{{c["id"]}}'>
								Preglej hranila
							</a>
						% else:
							Nima vnosov za hranila
						% end
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