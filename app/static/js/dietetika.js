$(document).ready(function(){

	var consumableNutrients = [];
	var $nutrientTable = $("#consumable_nutrients_table"); 
	var $nutrientTableWrapper = $nutrientTable.closest("#consumable_nutrients_table_wrapper"); 
	var $consumableForm = $("#consumable-modify");
	var $modifyType = $consumableForm.attr('data-modify-type');
	var consumableId = $("#consumable_id").val();

	setFormBootstrapValidator();

	setActiveNavigation();

	setAutoComplete();

	setFilterByConsumableType();

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
			consumableNutrients.push(json[i]);
			$nutrientTable.find("tbody").append(row);
		}
		
		hideShowTable($nutrientTableWrapper);
	}


	// MAIN FUNCTION FOR POSTING FORM
	$consumableForm.on("submit", function(ev){
		ev.preventDefault();

		var $errorsWrapper = $("#errors-wrapper");
		var $titleInput = $consumableForm.find("#title");
		var $consumableTypeSelect = $consumableForm.find("#consumable_type_select");
		var $caloriesInput = $consumableForm.find("#calories");

		var title = $titleInput.val();
		var consumableType = $consumableTypeSelect.val();
		var calories = $caloriesInput.val();


		// hide previous erros if exist
		$errorsWrapper.addClass("hidden");
		$errorsWrapper.find("li").remove();

		var errors = "";

		if (!title) {
			//TODO: add err wrapper and add field to insert title
			errors += "<li>Manjka ime izdelka.</li>";
		}
		if (consumableType == -1){
			errors += "<li>Manjka tip izdelka</li>";
		}
		if (!calories) {
			errors += "<li>Manjkajo kalorije</li>";
		}

		if (!title || consumableType == -1 || !calories) {
			// TODO: append errors to wrapper and show it
			$errorsWrapper.find("ul").append(errors);
			$errorsWrapper.removeClass("hidden");
			return;
		}

		// consumable json
		var consumableJson = {
			title: title,
			consumable_type_id: consumableType,
			calories: calories,
			nutrients: consumableNutrients
		};

		// consumable path
		var postUrl = "/consumable-enter";
		if ($modifyType == 'edit') {
			postUrl = "/consumable-edit/"+consumableId
		}
		
		$.ajax({
			type: "POST",
			url: postUrl,
			contentType: "application/json",
        	dataType: "json",
			data: JSON.stringify(consumableJson),
			success: function(data, status, xhr) {
				if (xhr.status == 200) {
					window.location.href = "/consumables";
				}
			},
			error: function(xhr, status, error) {
				// handle error
				console.error(error);
			}
		});
	});

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

	function manipulateSelectPristine(){
		$("select").attr('data-pristine', true);
		$("select").on("change", function(){
			$(this).removeAttr('data-pristine');
		})
	}
	function setFormBootstrapValidator() {
		$('form').validator({
			
		});
	}

	function setActiveNavigation(){
			var url = window.location.pathname;
		// Will only work if string in href matches with location
			$('ul.nav a[href="' + url + '"]').parent().addClass('active');
	
		// Will also work for relative and absolute hrefs
			$('ul.nav a').filter(function () {
				return this.href == url;
			}).parent().addClass('active').parent().parent().addClass('active');
	}

	function setAutoComplete() {
		// consumables
		$("#search-consumable-title #title").autocomplete({
			serviceUrl: '/consumables?isAjax=1'
		});
	}
	function setFilterByConsumableType() {
		$("#consumable_type_select").on("change", function(){
			var selected = $(this).val();
			if (selected != -1) {
				$(this).closest('form').submit();
			}
		})
	}

});