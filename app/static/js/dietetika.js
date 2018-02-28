$(document).ready(function () {

	// ko vnasamo/urejamo zivila se tukaj shranjujejo posamezna hranila
	var consumableNutrients = [];
	// reference na elemente ki potrebujemo
	var $nutrientTable = $("#consumable_nutrients_table");
	var $nutrientTableWrapper = $nutrientTable.closest("#consumable_nutrients_table_wrapper");
	var $consumableForm = $("#consumable-modify");
	var $modifyType = $consumableForm.attr('data-modify-type');
	var consumableId = $("#consumable_id").val();

	setFormBootstrapValidator();

	setActiveNavigation();

	setAutoComplete();

	setFilterByConsumableType();

	getSearchParametersOnConsumables();

	showHideGrowlMessage();

	// dodajanje hranil zivilu
	$("#add-nutrient-to-consumable").on("click", function (ev) {
		ev.preventDefault();

		//elements
		//select
		var $nutrientSelect = $("#nutrient");
		//input
		var $nutrientValueInput = $("#nutrient_value");


		// poisci podatke
		var nutrientId = $nutrientSelect.val();
		var nutrientValue = $nutrientValueInput.val();
		var nutrientTitle = $nutrientSelect.find('option[value="' + nutrientId + '"]').text();

		// izbrane morajo biti obe moznosti
		if (nutrientId != -1 && nutrientValue) {
			var nutrient = {
				id: nutrientId,
				title: nutrientTitle,
				value: nutrientValue
			};
			var tableRow = createNutrientsTableRow(nutrient);
			$nutrientTable.find("tbody").append(tableRow);
			//shranjujem tuple vrednosti
			consumableNutrients.push(nutrient);

			//reset vals
			$nutrientSelect.val(-1);
			$nutrientValueInput.val('');

			hideShowTable($nutrientTableWrapper);

		} 
	});

	// klik na odstrani hranilo na ustvarjanju/urejanju zivil
	$("#consumable_nutrients_table").on("click", "button[data-remove-nutrient]", function (ev) {
		ev.preventDefault();

		var nutrientId = $(this).attr("data-remove-nutrient");

		// odstrani vrstico v tabeli
		$("[data-remove-nutrient='" + nutrientId + "']").closest('tr').remove();

		// odstrani is seznama
		var nutrientIndex = consumableNutrients.indexOf(nutrientId);
		consumableNutrients.splice(nutrientIndex, 1);

		hideShowTable($nutrientTableWrapper);
	});

	// pri urejanju moramo najprej preveriti ali hranila ze obstajajo
	// te smo shranili v html attribute data-consumable-nutrients kot
	// json string katerega potem spremenimo v object in pridobimo podatke
	var existingNutrients = $($nutrientTable).attr('data-consumable-nutrients');
	if (existingNutrients) {
		var json = JSON.parse(existingNutrients);
		var row;
		for (var i = 0; i < json.length; i++) {
			row = createNutrientsTableRow(json[i]);
			consumableNutrients.push(json[i]);
			$nutrientTable.find("tbody").append(row);
		}

		hideShowTable($nutrientTableWrapper);
	}


	// glavna funkcija ki shranjuje spremembe na zivilih s pomocjo
	// ajax
	$consumableForm.on("submit", function (ev) {
		ev.preventDefault(); // ne gre na server

		var $errorsWrapper = $("#errors-wrapper");
		var $titleInput = $consumableForm.find("#title");
		var $consumableTypeSelect = $consumableForm.find("#consumable_type_select");
		var $caloriesInput = $consumableForm.find("#calories");

		var title = $titleInput.val();
		var consumableType = $consumableTypeSelect.val();
		var calories = $caloriesInput.val();


		// odstrani napake ce obstajajo
		$errorsWrapper.addClass("hidden");
		$errorsWrapper.find("li").remove();

		var errors = "";

		if (!title) {
			errors += "<li>Manjka ime izdelka.</li>";
		}
		if (consumableType == -1) {
			errors += "<li>Manjka tip izdelka</li>";
		}
		if (!calories) {
			errors += "<li>Manjkajo kalorije</li>";
		}

		if (!title || consumableType == -1 || !calories) {
			$errorsWrapper.find("ul").append(errors);
			$errorsWrapper.removeClass("hidden");
			return;
		}

		// consumable json
		// podatki ki se posljejo na server v json obliki
		// javastring object notation
		var consumableJson = {
			title: title,
			consumable_type_id: consumableType,
			calories: calories,
			nutrients: consumableNutrients
		};

		// consumable path
		var postUrl = "/consumables-enter";
		if ($modifyType == 'edit') {
			postUrl = "/consumable-edit/" + consumableId
		}

		// AJAX KLIC ki ustvari / posodobi zivila
		$.ajax({
			type: "POST",
			url: postUrl,
			contentType: "application/json",
			dataType: "json",
			data: JSON.stringify(consumableJson),
			success: function (data, status, xhr) {
				if (xhr.status == 200) {
					// k redirectu je potrebno dodan query parameter
					// da se prikaze "shranjeno" ali "posodobljeno"
					var redirect = "/consumables";
					if ($modifyType == 'edit') {
						redirect += "?changes=updated";
					} else if ($modifyType=="enter"){
						redirect += "?changes=created";
					}
					window.location.href = redirect;
				}
			},
			error: function (xhr, status, error) {
				// handle error
				console.error(error);
			}
		});
	});

	// ustvari vrstico v tabeli pri prikazu hranil posameznega zivila
	// ko se ustvarja ali posodablja zivilo
	function createNutrientsTableRow(nutrient) {
		var row = "<tr data-id='" + nutrient.id + "'>";
		row += "<td>" + nutrient.title + "</td>";
		row += "<td>" + nutrient.value + "</td>";
		row += "<td><button type='button' class='btn btn-danger glyphicon glyphicon-trash' data-remove-nutrient='" + nutrient.id + "'></button></td>";
		row += "</tr>";

		return row;
	}

	// prikaze tabelo hranil ce je ta prazna
	// oziroma jo prikaze ce ni prazna
	function hideShowTable($nutrientTableWrapper) {
		if (consumableNutrients && consumableNutrients.length) {
			$nutrientTableWrapper.removeClass('hidden');
		} else {
			$nutrientTableWrapper.addClass('hidden');
		}
	}

	function manipulateSelectPristine() {
		$("select").attr('data-pristine', true);
		$("select").on("change", function () {
			$(this).removeAttr('data-pristine');
		})
	}

	// bootstrap form validator
	function setFormBootstrapValidator() {
		$('form').validator({

		});
	}

	// nastavi vsebine vnosnih polj za iskanje na /consumables
	// glede na query parameter v urlju
	function getSearchParametersOnConsumables() {
		let searchParams = new URLSearchParams(window.location.search)
		var title = searchParams.get('title');
		var consumableType = searchParams.get('consumable_type_select');
		if (title) {
			// title exists / it was filtered by
			$("#search-consumable-title #title").val(title);
		}
		if (consumableType) {
			$("#consumable_type_select").val(consumableType);
		}
	}

	// nastavi active navbar povezavo glede na podstran na 
	// kateri se nahajamo
	function setActiveNavigation() {
		var url = window.location.pathname;

		if (url.endsWith('-enter')) {
			url = url.replace('-enter', '');
		}

		// Will only work if string in href matches with location
		$('ul.nav a[href="' + url + '"]').parent().addClass('active');

		// Will also work for relative and absolute hrefs
		$('ul.nav a').filter(function () {
			return this.href == url;
		}).parent().addClass('active').parent().parent().addClass('active');
	}

	// autocomplete na /consumables
	// in entry
	function setAutoComplete() {
		// consumables
		$("#entry-search input[type='text']").autocomplete({
			serviceUrl: '/consumables?isAjax=1'
		});
		$("#search-consumable-title #title").autocomplete({
			serviceUrl: '/consumables?isAjax=1'
		});
	}

	// dropdown, pri katerem si lahko izberemo
	// katere tipe zivil zelimo videti na /consumables
	function setFilterByConsumableType() {
		$("#consumable_type_select").on("change", function () {
			var selected = $(this).val();
			if (selected != -1) {
				$(this).closest('form').submit();
			}
		})
	}

	// prikaze in nato odstrani statusna sporocila kot 
	// so "ustvarjeno", "posodobljeno", "izbrisano"
	// glede na query parameter v urlju
	function showHideGrowlMessage() {
		var searchParams = new URLSearchParams(window.location.search)
		var changes = searchParams.get('changes');
		if (changes) {
			// nekaj se je zgodilo - create/update/delete
			var messageBox = $("#" + changes);
			messageBox.fadeIn();
			setTimeout(function () {
				messageBox.fadeOut();
			}, 1500);

		}
	}

});