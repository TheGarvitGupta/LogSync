$.ajaxSetup({
    cache: false
});

function render() {
	console.log("Rendering...");
	$.get("/renderTimeline", function(data, status) {
		$(".timeline").html(data);
	});
}

function filter(e) {
	alert(e.name + String(e.value));
}

$(document).ready(function(){
	render();

	// Add Log File button click
	$(".button").click(function(){
		
		var logPath = $('#logPath').val();
		var URL = '/addLog' + logPath;

    	$.get(URL, function(data, status) {
		
			console.log(status + ": " + data);
    		if (data.substring(0,3) == "+OK") {
    			render();
    		}
		});

	    $('#logPath').val("");
	});

	$("#logPath").click(function() { $(this).select(); } );
});