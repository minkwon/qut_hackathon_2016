var document = $('document'),
    loadSpinner = $('.spinner').hide(),
    data;

// size, margin of line chart
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

// function for Ajax request
var getJsonData = function (query) {
    $.getJSON('/home.json', {'query' : query},
        function(json) {
            data = JSON.parse(json);
        }
    );
};

// toggling visibility of loading spinner
$(document).ajaxStart(function () {
    loadSpinner.show();
}).ajaxStop(function () {
    loadSpinner.hide();
});

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
