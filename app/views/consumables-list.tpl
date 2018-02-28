%include('./base/header.tpl')
%include('./base/growl.tpl')
<div class="container main-content">

	<div class="anchors text-right">
		<a class='btn btn-primary' href='/consumables-enter'>Vnesi novega</a>
		<hr>
	</div>
	

	% if (len(consumables) != 0):

	<div class="search-wrapper row">
		<div class="col-sm-6">
			<form id='search-consumable-title' class="form-inline" method='GET'>
				<div class="form-group">
					<input type="text" placeholder='ime izdelka' class="form-control" id="title" name="title">
				</div>
				<button class='btn btn-default form-control' type="submit"><span class='glyphicon glyphicon-search'></span></button>
			</form>
		</div>
		<div class="col-sm-offset-3 col-sm-3 text-right">
			<form method='GET'>
				<div class="form-group">
					<select name="consumable_type_select" id="consumable_type_select" class='form-control'>
						<option value="-1"></option>
						% for ct in consumable_types:
						<option value="{{ct['id']}}">{{ct['title']}}</option>
						% end
					</select>
				</div>
			</form>			
		</div>
	</div>

	<table class="table table-striped">
		<thead>
		  <tr>
			<th>Živilo</th>
			<th>Tip živila</th>
			<th>Kalorije</th>
			<th>Vrednosti</th>
		  </tr>
		</thead>
		<tbody>
			% for c in consumables:
				<tr>
					<td>
						<a href='/consumable/{{c["id"]}}'>
							{{c['title']}}
						</a>
					</td>
					<td>
						{{c['consumable_type_title']}}
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