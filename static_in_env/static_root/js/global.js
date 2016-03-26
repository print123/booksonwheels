$(document).ready(function(){
	var typeaheadSource = ['John', 'Alex', 'Terry'];
	
	$('input.stext').typeahead({
		source: typeaheadSource
	});
});