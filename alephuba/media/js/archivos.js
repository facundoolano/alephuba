
function init_dialog() {
	$( "#dialog-modal" ).dialog({
		autoOpen: false,
		height: 140,
		modal: true,
		closeOnEscape : false,
		resizable : false,
		open: function(event, ui) { $(".ui-dialog-titlebar-close").hide(); }
	});
	
	$('form').submit(trigger_wait_message);
}

function trigger_wait_message() {
	$( "#dialog-modal" ).dialog('open');
}