function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

var update_site = function(poem_label, poem_text, fake_poem) {

    var random = getRandomInt(2);

    if (random == 0) {
        $("#first").html(poem_text);
        $("#first").attr("class", "rounded-lg shadow-md px-8 py-6 bg-white hover:shadow-lg hover:bg-gray-50 cursor-pointer text-left text-gray-900");
        var label = $("<p>")
            .attr("class", "hidden labels table text-xs font-semibold py-1 px-2 rounded text-green-600 bg-green-200 mb-2").html(poem_label)
            .attr("id", "real");
        $("#first").prepend(label);
        
        $("#second").html(fake_poem);
        $("#second").attr("class", "rounded-lg shadow-md px-8 py-6 bg-white hover:shadow-lg hover:bg-gray-50 cursor-pointer text-left text-gray-900");
        var label = $("<p>")
            .attr("class", "hidden labels table text-xs font-semibold py-1 px-2 rounded text-red-600 bg-red-200 mb-2").html("COMPUTER GENERATED")
            .attr("id", "fake");
        $("#second").prepend(label);
    }
    else {
        $("#first").html(fake_poem);
        $("#first").attr("class", "rounded-lg shadow-md px-8 py-6 bg-white hover:shadow-lg hover:bg-gray-50 cursor-pointer text-left text-gray-900");
        var label = $("<p>")
            .attr("class", "hidden labels table text-xs font-semibold py-1 px-2 rounded text-red-600 bg-red-200 mb-2").html("COMPUTER GENERATED")
            .attr("id", "fake");
        $("#first").prepend(label);

        $("#second").html(poem_text);
        $("#second").attr("class", "rounded-lg shadow-md px-8 py-6 bg-white hover:shadow-lg hover:bg-gray-50 cursor-pointer text-left text-gray-900");
        var label = $("<p>")
            .attr("class", "hidden labels table text-xs font-semibold py-1 px-2 rounded text-green-600 bg-green-200 mb-2").html(poem_label)
            .attr("id", "real");
        $("#second").prepend(label);
    }

    $("#next").removeClass("hidden");

}

var fetch_poems = function() {
    $("#first").empty();
    $("#first").html("Loading...");
    $("#first").attr("class", "rounded-lg shadow-md px-8 py-6 text-left bg-white text-gray-900")
    $("#second").empty();
    $("#second").html("Loading...");
    $("#second").attr("class", "rounded-lg shadow-md px-8 py-6 text-left bg-white text-gray-900")

    $("#next").addClass("hidden");
    $("#progress").removeClass("hidden");

    $("#progress_bar").css({ width: "5%" });
    $("#progress_bar").animate({ width: "15%" });
    setTimeout(
        function() { $("#progress_bar").animate({ width: "25%" }); },
    1000);
    setTimeout(
        function() { $("#progress_bar").animate({ width: "45%" }); },
    2000);
    setTimeout(
        function() { $("#progress_bar").animate({ width: "75%" }); },
    3000);

    $.ajax({

        type: "GET",
        url: "/fetch_poems",
        dataType : "json",
        contentType: "application/json; charset=utf-8",

        success: function(response){

            poem_label = response["poem_label"]
            poem_text = response["poem_text"]
            fake_poem = response["fake_poem"]

            update_site(poem_label, poem_text, fake_poem);

            $("#progress_bar").animate({ width: "100%" });

            setTimeout(
                function() { $('#progress').addClass("hidden"); }, 
            1000);

        },
        error: function(request, status, error) {
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }

    });
    
}

var evaluate_poems = function() {
    $(".labels").removeClass("hidden");
    if ($("#first").find("#real").length == 1) {
        console.log("SDF");
        $("#first").attr("class", "rounded-lg shadow-md px-8 py-6 bg-white text-left text-green-600");
        $("#second").attr("class", "rounded-lg shadow-md px-8 py-6 bg-white text-left text-red-600");
    }
    else {
        $("#first").attr("class", "rounded-lg shadow-md px-8 py-6 bg-white text-left text-red-600");
        $("#second").attr("class", "rounded-lg shadow-md px-8 py-6 bg-white text-left text-green-600");
    }
}

$(document).ready(function() {

    fetch_poems();

    $("#next").click(function() {
        fetch_poems();
    });

    $("#first").click(function() {
        evaluate_poems();
    });
    $("#second").click(function() {
        evaluate_poems();
    });

})
