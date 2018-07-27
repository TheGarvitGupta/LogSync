function log(data) {
	console.log(data);

	$("#logBox").fadeOut(0.5);
	window.setTimeout(addtext(data), 0.5);
	window.setTimeout(showLog, 0.5);
}

function addtext(data) {
	$("#logBox").html(data);
}

function showLog() {
	$("#logBox").fadeIn(0.5);
}

function addLog(e) {
	if (event.keyCode === 13) {
		$("#logAdd").click();
	}
}

$.ajaxSetup({
    cache: false
});

function render() {
	console.log("Rendering timeline...");
	$.get("/renderTimeline", function(data, status) {
		$(".timeline").html(data);
	});
}

function filter(e) {
	if (event.keyCode === 13) {
		var filterName = e.name;
		$.get( "/filter", { filePath: e.name, value: e.value } )
		.done(function(data, status) {
			log(data);
			if (data.substring(0,3) == "+OK") {
    			render();
    		}
		});
    }
}

$(document).ready(function(){
	render();
	// Add Log File button click
	$(".button").click(function(){
		var logPath = $('#logPath').val();
		if(logPath.substring(0,1) == "/") {
			logPath = logPath.substring(1, logPath.length);
		}
		var URL = '/addLog/' + logPath;
    	$.get(URL, function(data, status) {
			log(data);
    		if (data.substring(0,3) == "+OK") {
    			render();
    		}
		});
	    $('#logPath').val("");
	});
	$("#logPath").click(function() { $(this).select(); } );
});