var document = $("document"),
    loadSpinner = $('.spinner'),
    simulation;

// size, margin of line chart
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 1100 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom,
    centreX = width / 2 + margin.left,
    centreY = height / 2 + margin.top;

// setting up the frame
var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// tag overview force simulation
function simulateTagOverview(data) {
    var maxCount = d3.max(data, function(d) { return d.totalCount; });
    var nodeSizeScale = d3.scaleLinear()
        .domain([1000, maxCount])
        .rangeRound([3, 60]);

    var colorScale = d3.scaleLinear()
        .domain([1000, maxCount])
        .range(["yellow", "red"]);

    simulation = d3.forceSimulation(data)
        // positive attracts negative repels each other
        //.force("charge", d3.forceManyBody(-10).distanceMax(50))

        // only modifies position of nodes, not the velocity
        .force("centre", d3.forceCenter(centreX,centreY - 20))
        // collision, stops nodes from overlapping, essentially a radius
        .force("collision", d3.forceCollide(function(d) {
            return nodeSizeScale(d.totalCount) + 2;
        }))
        .force("x", d3.forceX(0.01))
        .force("y", d3.forceY(0.01))
        // atmospheric friction, defaults to 0.9
        .velocityDecay("0.5");

    // creating nodes
    var node = svg.selectAll('.node')
        .data(data)
        .enter()
        .append('circle')
        .attr('fill', function(d) { return colorScale(d.totalCount) })
        .attr('r', function(d) { return nodeSizeScale(d.totalCount); })
        .classed('.node', true);

    // call back function when the simulation calculation ends
    // and the data is populated with force simulation variables
    simulation.on('end', function() {
        node.attr('cx', function(d) { return d.x; })
            .attr('cy', function(d) { return d.y; });
        console.log("end")
    })
        .on("tick", function() {
            node.attr('cx', function(d) { return d.x; })
                .attr('cy', function(d) { return d.y; });
        });
}

function stopSimulation() {
    simulation.stop();
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