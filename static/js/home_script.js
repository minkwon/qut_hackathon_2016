var document = $("document"),
    loadSpinner = $('.spinner'),
    nodes,
    simulation;

// hard-coded tag count
var currentTotalTagCount = 3221;

// size, margin of line chart
var margin = {top: 10, right: 50, bottom: 10, left: 50},
    width = 1400 - margin.left - margin.right,
    height = 850 - margin.top - margin.bottom,
    centreX = width / 2 + margin.left,
    centreY = height / 2 + margin.top;

// setting up the frame
var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

var infoBox = svg.append("g")
    .style("opacity", 0)
    .attr("id", "infoBox");

var title = infoBox.append("text")
    .attr("x", 0)
    .attr("y", 50)
    .attr("font-size", 40)
    .html("How large is StackOverflow Data?");

infoBox.append("text")
    .attr("x", 0)
    .attr("y", 150)
    .attr("font-size", 28)
    .html("13 Million Questions and 22 Million Answers");

infoBox.append("text")
    .attr("x", 0)
    .attr("y", 220)
    .attr("font-size", 28)
    .html("7 Million Active User Accounts");

infoBox.append("text")
    .attr("x", 0)
    .attr("y", 290)
    .attr("font-size", 28)
    .html("47,064 Tags available for use");

infoBox.append("text")
    .attr("x", 0)
    .attr("y", 360)
    .attr("font-size", 28)
    .html("25 Billion Total Views");

infoBox.append("text")
    .attr("x", 0)
    .attr("y", 430)
    .attr("font-size", 28)
    .html("8 Years of Accumulated Database");

infoBox.append("text")
    .attr("x", 0)
    .attr("y", 680)
    .attr("font-size", 20)
    .html("*Figures were queried at StackExchange Data Explorer on 22/05/2017");

var tooltip = d3.tip().attr("class", "d3-tip")
    .attr("id", "home-tooltip")
    .offset([-10, 0])
    .html(function(d, i) {
        return "<strong>Tag name:</strong> <span style='color:white'>" + d.tagName + "</span><br>"
            + "<strong>Rank:</strong> <span style='color:white'>" + (currentTotalTagCount - i) + "</span><br>"
            + "<strong>Frequency:</strong> <span style='color:white'>" + d.totalCount + "</span>";
    });

// tag overview force simulation
function simulateTagOverview(data) {
    var maxCount = d3.max(data, function(d) { return d.totalCount; });
    var nodeSizeScale = d3.scaleLinear()
        .domain([1000, maxCount])
        .rangeRound([3, 60]);

    var colorScale = d3.scaleLinear()
        .domain([1000, (maxCount - 1000) / 2 + 1000, maxCount])
        .range(["white", "orange", "red"]);

    simulation = d3.forceSimulation(data)
        // positive attracts negative repels each other
        //.force("charge", d3.forceManyBody(-10).distanceMax(50))

        // only modifies position of nodes, not the velocity
        .force("centre", d3.forceCenter(centreX - 200,centreY - 50))
        // collision, stops nodes from overlapping, essentially a radius
        .force("collision", d3.forceCollide(function(d) {
            return nodeSizeScale(d.totalCount) + 2;
        }))
        .force("x", d3.forceX(0.001))
        .force("y", d3.forceY(0.001))
        // atmospheric friction, defaults to 0.9
        .velocityDecay("0.85");

    // creating nodes
    nodes = svg.selectAll('.node')
        .data(data)
        .enter()
        .append('circle')
        .attr('fill', function(d) { return colorScale(d.totalCount) })
        .attr('stroke-width', 3)
        .attr('stroke', function(d) { return d3.color(colorScale(d.totalCount)).darker()})
        .attr('r', function(d) { return nodeSizeScale(d.totalCount); })
        .classed('.node', true)
        .call(tooltip)
        .on('mouseover', tooltip.show)
        .on('mouseout', tooltip.hide);

    // call back function when the simulation calculation ends
    simulation.on('end', function() {
        stopSimulation();
    })
        // call back function for every tick
        .on("tick", function() {
            nodes.attr('cx', function(d) { return d.x; })
                .attr('cy', function(d) { return d.y; });
        });
}

/*
    When simulation ended by itself or by a button pressed
    The diagram moves to the right and shows tooltops
 */
function stopSimulation() {
    simulation.stop();
    nodes.transition()
            .attr('cx', function(d) { return d.x + 300; })
            .attr('cy', function(d) { return d.y; });
    showText()
}

function showText() {
    infoBox.transition()
        .style("opacity", 1)
        .duration(400);
}

// Ajax call for total count nodes
$.getJSON('/home.json', {'query' : "totalCount"},
    function(json) {
        var data = JSON.parse(json);
        simulateTagOverview(data);
    }
);

// toggling visibility of loading spinner during ajax request
$(document).ajaxStart(function () {
    // ajax start
    loadSpinner.show();
}).ajaxStop(function () {
    loadSpinner.hide();
});