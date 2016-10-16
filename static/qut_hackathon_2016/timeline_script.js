var document = $('document'),
    loadSpinner = $('.spinner').hide(),
    chartDrawn = false;

// size, margin of line chart
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Add the X Axis
svg.append("g")
    .classed("xaxis", true)
    .attr("transform", "translate(0," + height + ")");

// Add the Y Axis
svg.append("g")
    .classed("yaxis", true);

// Add line group
var lines = svg.append("g").attr("id", "lines");

// Trend line color scale
var trendLineColor = d3.scaleOrdinal(d3.schemeDark2).domain(d3.range(0, 8));

// Tool tip initialised
var toolTip = d3.select('body').append('div')
    .classed("tooltip", true)
    .style('position', 'absolute')
    .style('padding', '0 10px')
    .style('background', 'white')
    .style('opacity', 0);

// vertical guide
var verticalGuide = d3.select('#lines').append('path')
    .attr("position", "relative")
    .attr("stroke", "black")
    .style('stroke-width', 2)
    .style('opacity', 0)
    .attr("d", "M0 0 V " + height);

function refreshChart(data) {

    if (chartDrawn) {
        d3.selectAll('.line').remove();
    }
    var dates = [];
    var maxValue = 0;
    var parseTime = d3.timeParse("%Y-%m");

    // format the dates and save in dates, also find max value amongst all data
    for (var i = 0; i < data.length; i++){
        var entry = data[i];
        for (var key in entry) {
            if (entry.hasOwnProperty(key)) {
                if (key === "date") {
                    dates.push(parseTime(entry[key]));
                } else if (entry[key] > maxValue) {
                    maxValue = entry[key];
                }
            }
        }
    }

    // Set scaling
    var xScale = d3.scaleTime().rangeRound([0, width]);
    var yScale = d3.scaleLinear().range([height, 0]);
    xScale.domain([new Date(2009, 3, 0), new Date(2016, 6, 0)]);
    yScale.domain([0, maxValue]);

    // iterator for trend line color
    i = 0;

    // Add lines
    // entry == { "date" : "2016-06", "java" : 123, "c" : 456 }
    for (key in entry) {
        if (entry.hasOwnProperty(key) && key != 'date') {
            var line = d3.line()
                            .x(function(d, i) {
                                return xScale(dates[i]);
                            })
                            .y(function(d) {
                                return yScale(d[key]);
                            });

            console.log("key is " + key);
            lines.append('path')
                .data([data])
                .attr("class", "line")
                .style("stroke", trendLineColor(i))
                .attr("d", line);
        }
        i++;
    }

    // Update axes with new data
    svg.select('.xaxis')
        .call(d3.axisBottom(xScale).ticks(d3.timeMonth.every(6)));
    svg.select('.yaxis')
        .call(d3.axisLeft(yScale));

    chartDrawn = true;

    // initialise tooltip
    d3.select('svg')
        .on("mousemove", function() {
            toolTip.style('opacity', 0.9)
            .html("hello fucking world");
            toolTip.style('left', (d3.event.pageX + 30) + 'px')
                .style('top', (d3.event.pageY + 30) + 'px');

            verticalGuide
                .style('stroke', 'orange')
                .style('opacity', 1)
                .attr("d", "M" + (d3.event.pageX - margin.left) + " 0 V " + height)
        })
        .on("mouseleave", function() {
            toolTip.style('opacity', 0);

            verticalGuide.transition()
                .attr("d", "M0 0 V " + height)
                .style("stroke", 'black')
                .delay(100)
                .style("opacity", 0)
        })

}

// Ajax call when enter key is pressed
$(document).ready(function(){
    var search = $('#search');
    search.keypress(function(e){
        // If enter key pressed
        if(e.which == 13){
            $.getJSON('/timeline.json', {'query' : search.val()},
                function (json) {
                    var data = JSON.parse(json);
                    refreshChart(data);
                });
            search.val('');
        }
    });
});

// toggling visibility of loading spinner
$(document).ajaxStart(function () {
    loadSpinner.show();
}).ajaxStop(function () {
    loadSpinner.hide();
});