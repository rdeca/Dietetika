$(document).ready(function(){

	var consumableNutrients = [];
	var $nutrientTable = $("#consumable_nutrients_table"); 
	var $nutrientTableWrapper = $nutrientTable.closest("#consumable_nutrients_table_wrapper"); 

	// bind add nutrient to consumable
	$("#add-nutrient-to-consumable").on("click", function(ev){
		ev.preventDefault();

		//elements
		//select
		var $nutrientSelect = $("#nutrient");
		//input
		var $nutrientValueInput = $("#nutrient_value");


		// find data
		var nutrientId = $nutrientSelect.val();
		var nutrientValue = $nutrientValueInput.val();
		var nutrientTitle = $nutrientSelect.find('option[value="'+nutrientId+'"]').text();

		// check that both options were selected
		if (nutrientId != -1 && nutrientValue) {
			var nutrient = {
				id: nutrientId,
				title: nutrientTitle,
				value: nutrientValue
			};
			var tableRow = createNutrientsTableRow(nutrient);
			$nutrientTable.find("tbody").append(tableRow);
			consumableNutrients.push(nutrient);

			//reset vals
			$nutrientSelect.val(-1);
			$nutrientValueInput.val('');

			hideShowTable($nutrientTableWrapper);
			
		} else {
			//TODO: show err that stuff needs to be selected
		}
	});

	//bind remove nutrient
	$("#consumable_nutrients_table").on("click", "button[data-remove-nutrient]", function(ev){
		ev.preventDefault();

		var nutrientId = $(this).attr("data-remove-nutrient");
		
		//remove nutrient row
		$("[data-remove-nutrient='"+nutrientId+"']").closest('tr').remove();

		//remove from array
		var nutrientIndex = consumableNutrients.indexOf(nutrientId);
		consumableNutrients.splice(nutrientIndex, 1);

		hideShowTable($nutrientTableWrapper);
	});

	// check if on edit there are nutrients already appended
	// so we need to fill the table
	var existingNutrients = $($nutrientTable).attr('data-consumable-nutrients');
	if (existingNutrients) {
		var json = JSON.parse(existingNutrients);
		var row;
		for (var i = 0; i<json.length; i++) {
			row = createNutrientsTableRow(json[i]);
			consumableNutrients.push(json[i].id);
			$nutrientTable.find("tbody").append(row);
		}
		
		hideShowTable($nutrientTableWrapper);
	}

	function createNutrientsTableRow(nutrient){
		var row = "<tr data-id='" + nutrient.id + "'>";
		row += "<td>" + nutrient.title + "</td>";
		row += "<td>" + nutrient.value + "</td>";
		row += "<td><button type='button' class='btn btn-danger glyphicon glyphicon-trash' data-remove-nutrient='"+nutrient.id+"'></button></td>";
		row += "</tr>";

		return row;
	}

	function hideShowTable($nutrientTableWrapper) {
		if (consumableNutrients && consumableNutrients.length) {
			$nutrientTableWrapper.removeClass('hidden');
		} else {
			$nutrientTableWrapper.addClass('hidden');
		}
	}

});