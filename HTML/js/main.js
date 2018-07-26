$.ajaxSetup({
    cache: false
});

function render() {
	console.log("Rendering...");
	$.get("/renderTimeline", function(data, status) {
		$(".timeline").html(data);
	});
}

$(document).ready(function(){
	render();

	// Add Log File button click
	$(".button").click(function(){
		
		var logPath = $('#logPath').val();
		var URL = '/addLog' + logPath;

    	$.get(URL, function(data, status) {
		
			// alert(status + ": " + data);
    		if (data == "+OK") {
    			render();
    		}
    		else{
    			// alert(status + ": " + data);
    		}
		});

	    $('#logPath').val("");
	});

	$("#logPath").click(function() { $(this).select(); } );
});