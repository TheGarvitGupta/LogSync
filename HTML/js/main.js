$(".button").click(function(){
    $.get("/getFile", function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
    });
});