var loadSpinner = $('.spinner');
loadSpinner.hide();

var dataCache;
// toggling visibility of loading spinner
$(document).ajaxStart(function () {
    loadSpinner.show();
}).ajaxStop(function () {
    loadSpinner.hide();
});

var margin = {top: 20, right: 50, bottom: 30, left: 65},
    width = $("#stacked-chart-pane").width() - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var svg = d3.select("#stacked-chart-pane").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("data-zoomscale", 1)
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// clip path
svg.append("clipPath").attr("id", "clip").append("rect").attr("width", width).attr("height", height);

// Add line group
var lines = svg.append("g").attr("id", "lines");

var yAxisTextLabel = svg.append("text").attr("x", "-28").attr("y", height / 2).attr("text-anchor", "end");

var parseTime = d3.timeParse("%Y-%m");
var formatTime = d3.timeFormat("%B %Y");
var bisectDate = d3.bisector(function(d) { return parseTime(d.date); }).right;

// Tool tip initialised
var toolTip = d3.select('body').append('div')
    .attr("class", "d3-tip")
    .attr("id", "questions-tooltip")
    .style('position', 'absolute')
    .style('opacity', 0);

// vertical guide
var verticalGuide = d3.select('#lines').append('path')
    .attr("position", "relative")
    .attr("stroke", "black")
    .style('stroke-width', 2)
    .style('opacity', 0)
    .attr("d", "M0 0 V " + height);

var formerTagLabel = svg.append("text")
        .attr("x", width - 20)
        .attr("y", 30)
        .attr("text-anchor", "end")
        .attr("font-family", "Verdana")
        .attr("font-size", "35");
var latterTagLabel = svg.append("text")
        .attr("x", width - 20)
        .attr("y", height - 30)
        .attr("text-anchor", "end")
        .attr("font-family", "Verdana")
        .attr("font-size", "35");

var chartDrawn = false;

function refreshChart(data) {
    dataCache = JSON.parse(JSON.stringify(data));
    if (chartDrawn) {
        d3.selectAll('.area').remove();
        d3.selectAll('.xaxis').remove();
        d3.selectAll('.yaxis').remove();
        d3.selectAll('g.graph').remove();
    }
    var former = data["former"];
    var latter = data["latter"];

    // Set scaling
    var xScale = d3.scaleTime().rangeRound([0, width]);
    var y0Scale = d3.scaleLinear().range([height / 2, 0]);
    var y1Scale = d3.scaleLinear().range([height / 2, height]);
    var y0DayScale = d3.scaleLinear().range([height / 2, 0]);
    var y1DayScale = d3.scaleLinear().range([height / 2, height]);

    var earliestTime = d3.min([d3.min(former.series, function(d) {
        return parseTime(d.date);
    }), d3.min(latter.series, function(d) {
        return parseTime(d.date);
    })]);

    var latestTime = d3.max([d3.max(former.series, function(d) {
        return parseTime(d.date);
    }), d3.max(latter.series, function(d) {
        return parseTime(d.date);
    })]);
    var zoomedDomainDate = xScale.invert(xScale(earliestTime) * svg.attr("data-zoomscale"));

    xScale.domain([zoomedDomainDate, latestTime]);
    var maxValue = updateMaxValue(former, latter, zoomedDomainDate);

    y0Scale.domain([0, maxValue]);
    y1Scale.domain([0, maxValue]);
    y0DayScale.domain([0, maxValue / 86400]);
    y1DayScale.domain([0, maxValue / 86400]);

    var areaUpFirstAnswer = d3.area().x(function(d) {
        return xScale(parseTime(d.date)); })
        .y0(height / 2)
        .y1(function(d) { return y0Scale(getAverageTimeForFirstAnswered(d.data)); });

    var areaUpFirstAnswerBorder = d3.line().x(function(d) {
        return xScale(parseTime(d.date)); })
        .y(function(d) { return y0Scale(getAverageTimeForFirstAnswered(d.data)); });

    var areaUpAccepted = d3.area().x(function(d) { return xScale(parseTime(d.date)); })
        .y0(height / 2)
        .y1(function(d) { return y0Scale(getAverageTimeForAcceptedAnswer(d.data)); });

    var areaUpAcceptedBorder = d3.line().x(function(d) { return xScale(parseTime(d.date)); })
        .y(function(d) { return y0Scale(getAverageTimeForAcceptedAnswer(d.data)); });

    var areaDownFirstAnswer = d3.area().x(function(d) { return xScale(parseTime(d.date)); })
        .y0(height / 2)
        .y1(function(d) { return y1Scale(getAverageTimeForFirstAnswered(d.data)); });

    var areaDownFirstAnswerBorder = d3.line().x(function(d) { return xScale(parseTime(d.date)); })
        .y(function(d) { return y1Scale(getAverageTimeForFirstAnswered(d.data)); });

    var areaDownAccepted = d3.area().x(function(d) { return xScale(parseTime(d.date)); })
        .y0(height/ 2)
        .y1(function(d) { return y1Scale(getAverageTimeForAcceptedAnswer(d.data)); });

    var areaDownAcceptedBorder = d3.line().x(function(d) { return xScale(parseTime(d.date)); })
        .y(function(d) { return y1Scale(getAverageTimeForAcceptedAnswer(d.data)); });

    var graph = svg.append("g").attr("class", "graph");

    graph.append("path")
        .data([former.series])
        .attr("class", "area")
        .attr("id", "areaUp0")
        .attr("opacity", 0.7)
        .attr("d", areaUpFirstAnswer)
        .attr("clip-path", "url(#clip)");

    graph.append("path")
        .data([former.series])
        .attr("class", "area")
        .attr("id", "areaUp1")
        .attr("opacity", 0.7)
        .attr("d", areaUpAccepted)
        .attr("clip-path", "url(#clip)");

    graph.append("path")
        .data([latter.series])
        .attr("class", "area")
        .attr("id", "areaDown0")
        .attr("opacity", 0.95)
        .attr("d", areaDownFirstAnswer)
        .attr("clip-path", "url(#clip)");

    graph.append("path")
        .data([latter.series])
        .attr("class", "area")
        .attr("id", "areaDown1")
        .attr("opacity", 0.3)
        .attr("d", areaDownAccepted)
        .attr("clip-path", "url(#clip)");

    graph.append("path")
        .data([former.series])
        .attr("class", "area")
        .attr("id", "areaUp0-border")
        .attr("fill-opacity", 0)
        .attr("d", areaUpFirstAnswerBorder)
        .attr("clip-path", "url(#clip)");

    graph.append("path")
        .data([former.series])
        .attr("class", "area")
        .attr("id", "areaUp1-border")
        .attr("fill-opacity", 0)
        .attr("d", areaUpAcceptedBorder)
        .attr("clip-path", "url(#clip)");

    graph.append("path")
        .data([latter.series])
        .attr("class", "area")
        .attr("id", "areaUp0-border")
        .attr("fill-opacity", 0)
        .attr("d", areaDownFirstAnswerBorder)
        .attr("clip-path", "url(#clip)");

    graph.append("path")
        .data([latter.series])
        .attr("class", "area")
        .attr("id", "areaUp1-border")
        .attr("fill-opacity", 0)
        .attr("d", areaDownAcceptedBorder)
        .attr("clip-path", "url(#clip)");

    // Update axes with new data
    svg.append("g").attr('class', 'xaxis')
        .attr("transform", "translate(0," + (height / 2) + ")")
        .call(d3.axisBottom(xScale));
    svg.append("g").attr('class', 'yaxis').attr('id', 'y0axis')
        .call(d3.axisLeft(y0DayScale));
    svg.append("g").attr('class', 'yaxis').attr('id', 'y1axis')
        .call(d3.axisLeft(y1DayScale));

    chartDrawn = true;

    d3.select(".xaxis").selectAll("text").attr("dy", function() {
            if (!isNaN(this.innerHTML)) {
                return "1.2em";
            }
            return "0.7em";
        })
        .attr("font-weight", function() {
            if (!isNaN(this.innerHTML)) {
                return "bolder";
            }
            return "normal"
        })
        .attr("font-size", "18px");

    // mouse event on the line chart
    d3.select('svg')
        .on("mousemove", function() {
            var mouseX = Math.min(d3.mouse(this)[0] - margin.left, width);
            if (mouseX < 0 || mouseX > width - 1) {
                return;
            }
            var mouseDate = xScale.invert(mouseX);
            var mouseDataIndexFormer = bisectDate(former.series, mouseDate);
            var mouseDataIndexLatter = bisectDate(latter.series, mouseDate);
            // tool tip
            if (d3.event.pageX < $(window).width() - 180) {
                toolTip.style('left', (d3.event.pageX + 10) + 'px')
                .style('top', (d3.event.pageY + 35) + 'px');
            } else {
                toolTip.style('left', (d3.event.pageX - 180) + 'px')
                .style('top', (d3.event.pageY + 35) + 'px');
            }

            toolTip.style('opacity', 0.9)
                .html("Date: ")
                .append("span")
                .html(formatTime(mouseDate) + "<br><br>");

            var correctAnswerSection = toolTip.append("div");
            var firstAnswerSection = toolTip.append("div");

            correctAnswerSection.style("text-align", "right").style("background", "rgb(94, 186, 125)")
                .style("padding", "2px")
                .style("margin", "2px")
                .attr("opacity", "1")
                .html(former.name + " : " + prettyPrint(getAverageTimeForAcceptedAnswer(former.series[mouseDataIndexFormer].data)) + "<br>"
                    + latter.name + " : " + prettyPrint(getAverageTimeForAcceptedAnswer(latter.series[mouseDataIndexLatter].data)));
            firstAnswerSection.style("text-align", "right").style("background", "rgb(244, 128, 36)")
                .style("padding", "2px")
                .style("margin", "2px")
                .html(former.name + " : " + prettyPrint(getAverageTimeForFirstAnswered(former.series[mouseDataIndexFormer].data)) + "<br>"
                    + latter.name + " : " + prettyPrint(getAverageTimeForFirstAnswered(latter.series[mouseDataIndexLatter].data)));
            verticalGuide
                .style('stroke', 'orange')
                .style('opacity', 1)
                .attr("d", "M" + (d3.mouse(this)[0] - margin.left) + " 0 V " + height)
        })
        .on("mouseleave", function() {
            toolTip.style('opacity', 0);

            verticalGuide.transition()
                .attr("d", "M0 0 V " + height)
                .style("stroke", 'black')
                .delay(100)
                .style("opacity", 0)
        });

    formerTagLabel.html(former.name);
    latterTagLabel.html(latter.name);
    if (yAxisTextLabel.html() == "") {
        yAxisTextLabel.html("Days");
        var legend = svg.append("g").attr("id", "legend");

        legend.append("rect").attr("x", width / 2 - 150).attr("y", height - 22)
            .attr("width", 20)
            .attr("height", 20)
            .style("fill", "rgb(94, 186, 125)")
            .attr("opacity", 0.7);

        legend.append("text")
            .attr("x", width / 2 - 125)
            .attr("y", height + 16 - 22)
            .attr("font-size", "16px")
            .html("Average time it takes for an acceptable answer");

        legend.append("rect").attr("x", width / 2 - 150).attr("y", height)
            .attr("width", 20)
            .attr("height", 20)
            .style("fill", "rgb(244, 128, 36)")
            .attr("opacity", 0.7);

        legend.append("text")
            .attr("x", width / 2 - 125)
            .attr("y", height + 16)
            .attr("font-size", "16px")
            .html("Average time it takes for a first answer");

    }
}

function inputEmpty() {
    if ($("#former-tag-box").val() == "" || $("#latter-tag-box").val() == "") {
        return true;
    }
    return false;
}

// Ajax call when enter key is pressed
$(document).ready(function(){
    $("input[type=text]").keypress(function(e){
        // If enter key pressed
        if(e.which == 13){
            if (inputEmpty()) {
                return;
            }
            if (inputInvalid()) {
                alert("Input is not a valid tag");
                return;
            }
            var query = {"former" : $("#former-tag-box").val(), "latter" : $("#latter-tag-box").val()};
            $.getJSON('/questions.json/', query,
                function (json) {
                    svg.attr("data-zoomscale", 1);
                    refreshChart(json);
                    svg.transition().duration(2000).attr("data-zoomscale", 1.25).on("end", function() {
                        zoom.scaleTo(svg, 1.25);
                    }).tween("side-effects", function() {
                        return function() {
                            refreshChart(json);
                        }
                    });
                }
            );
        }
    });
});

// auto-complete
$('input').autoComplete({
    minChars: 2,
    source: function(term, suggest) {
        term = term.toLowerCase();
        var choices = tags;
        var matches = [];
        for (i=0; i<choices.length; i++)
            if (~choices[i].toLowerCase().indexOf(term)) matches.push(choices[i]);
        suggest(matches);
    }
});

function inputInvalid() {
    var choices = tags;
    var formerTagInput = $("#former-tag-box").val().toLowerCase();
    var latterTagInput = $("#latter-tag-box").val().toLowerCase();
    if (choices.indexOf(formerTagInput) != -1 && choices.indexOf(latterTagInput) != -1) {
        return false;
    }
    return true;
}

function getAverageTimeForFirstAnswered(d) {
    if (d[1] == 0) {
        return 0;
    }
    return d[3] / d[1];
}

function getAverageTimeForAcceptedAnswer(d) {
    if (d[2] == 0) {
        return 0;
    }
    return d[4] / d[2];
}

window.onresize = function(event) {
    width = $("#stacked-chart-pane").width() - margin.left - margin.right;
    d3.select('svg').attr("width", width + margin.left + margin.right);
    d3.select('#clip rect').attr("width", width).attr("height", height);
    if (dataCache !== undefined) {
        refreshChart(dataCache);
    }
};

var zoom = d3.zoom().scaleExtent([1,1.25])
    .on("zoom", scrollZoom);
svg.call(zoom);

function scrollZoom() {
    var transform = d3.zoomTransform(svg.node());
    svg.attr("data-zoomscale", transform.k);
    if (dataCache !== undefined) {
        refreshChart(dataCache);
    }
}

function updateMaxValue(former, latter, zoomedDomainDate) {
    var formerBisect = bisectDate(former.series, zoomedDomainDate);
    var latterBisect = bisectDate(latter.series, zoomedDomainDate);
    var maxValue = 0;
    former["series"].forEach(function(d, i) {
        if (i < formerBisect) {
            return;
        }
        if (getAverageTimeForFirstAnswered(d.data) > maxValue) {
            maxValue = getAverageTimeForFirstAnswered(d.data);
        }
        if (getAverageTimeForAcceptedAnswer(d.data) > maxValue) {
            maxValue = getAverageTimeForAcceptedAnswer(d.data);
        }
    });

    latter["series"].forEach(function(d, i) {
        if (i < latterBisect) {
            return;
        }
        if (getAverageTimeForFirstAnswered(d.data) > maxValue) {
            maxValue = getAverageTimeForFirstAnswered(d.data);
        }
        if (getAverageTimeForAcceptedAnswer(d.data) > maxValue) {
            maxValue = getAverageTimeForAcceptedAnswer(d.data);
        }
    });
    return maxValue;
}

function prettyPrint(seconds) {
    if (seconds / 86400 < 1) {
        return (seconds / 3600).toFixed(2) + " hours";
    }
    return (seconds / 86400).toFixed(2) + " days";
}