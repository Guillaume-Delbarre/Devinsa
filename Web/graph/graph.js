var margin = {top: 60, right: 40, bottom: 88, left: 100},
  width = 1000 - margin.left - margin.right,
  height = 650 - margin.top - margin.bottom;

var x = d3.scale.linear()
  .range([0, width]);

var y = d3.scale.linear()
  .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
  .scale(x)
  .orient("bottom");

var yAxis = d3.svg.axis()
  .scale(y)
  .orient("left");

var svg = d3.select("body")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom);

var shiftKey;

var rect, 
node;

svg = svg.append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var selection = [];

function get_selection(){
  selection = [];
  node.each(function(d) {
    if (d.selected) {
       selection.push(d);
    }
  });
  console.log(selection);
}

function clear_selection() {
  node.classed('selected', function (d) { return d.selected = false; })
}

d3.csv("https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/Donnees/resPCA.csv", function(error, data) {
  data.forEach(function(d) {
    d.Axe_X = +d.Axe_X;
    d.Axe_Y = +d.Axe_Y;
    d.Medoid = +d.Medoid;
  });

  x.domain(d3.extent(data, function(d) { return d.Axe_X; })).nice();
  y.domain(d3.extent(data, function(d) { return d.Axe_Y; })).nice();

  svg = svg.call(d3.behavior.zoom().x(x).y(y).on("zoom", zoom));

  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)

  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)

  var brush = svg.append("g")
    .datum(function() { return {selected: false, previouslySelected: false}; })
    .attr("class", "brush")
    .call(d3.svg.brush()
      .x(d3.scale.identity().domain([0, width]))
      .y(d3.scale.identity().domain([0, height]))
      .on("brushstart", function(d) {
        console.log('brushstart');
        node.each(function(d) { d.previouslySelected = shiftKey && d.selected; });
        if (!shiftKey) {
          d3.event.target.clear();
          d3.select(this).call(d3.event.target);
        }
      })
      .on("brush", function() {
        if (shiftKey) {
          console.log('shiftKey', shiftKey);
          var extent = d3.event.target.extent();
          node.classed("selected", function(d) {
            return d.selected = d.previouslySelected ^
            (extent[0][0] <= x(d.Axe_X) && x(d.Axe_X) < extent[1][0]
              && extent[0][1] <= y(d.Axe_Y) && y(d.Axe_Y) < extent[1][1]);
          });
        } else {
          d3.event.target.clear();
          d3.select(this).call(d3.event.target);
        }
      })
      .on("brushend", function() {
        d3.event.target.clear();
        d3.select(this).call(d3.event.target);
      }));

  function zoom() {
    if (shiftKey) { 
      console.log('zoom shiftKey');
      return;
    }
    console.log('zoom');
    node.attr("cx", function(d) { return x(d.Axe_X); })
    .attr("cy", function(d) { return y(d.Axe_Y); });
    d3.select('.x.axis').call(xAxis);
    d3.select('.y.axis').call(yAxis);
  }

  rect = svg.append('rect')
    .attr('pointer-events', 'all')
    .attr('width', width)
    .attr('height', height)
    .style('fill', 'none');
  
  node = svg.selectAll(".dot")
    .data(data)
    .enter().append("circle")
    .attr("class", "dot")
    .attr("r", function(d) { return d.selected ? 5 : 7; })
    .attr("cx", function(d) { return x(d.Axe_X); })
    .attr("cy", function(d) { return y(d.Axe_Y); })
    .style("fill", function(d) { return color(d.Cluster); })
    .on("mousedown", function(d) {
      if (shiftKey) {
        d3.select(this).classed("selected", d.selected = !d.selected);
      } else {
        node.classed("selected", function(p) {
          return p.selected = d === p;
        });
      }
    });

  node.classed('selected', function (d) {return d.selected;})

  var legend = svg.selectAll(".legend")
    .data(color.domain())
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
    .attr("x", width - 18)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", color);

  legend.append("text")
    .attr("x", width - 24)
    .attr("y", 9)
    .attr("dy", ".35em")
    .style("text-anchor", "end")
    .text(function(d) { return d; });
  
    d3.select(window).on("keydown", function() {
      shiftKey = d3.event.shiftKey;
      if (shiftKey) {
        rect = rect.attr('pointer-events', 'none');
      } else {
        rect = rect.attr('pointer-events', 'all');
      }
    });
  
    d3.select(window).on("keyup", function() {
      shiftKey = d3.event.shiftKey;
      if (shiftKey) {
        rect = rect.attr('pointer-events', 'none');
      } else {
        rect = rect.attr('pointer-events', 'all');
      }
    });
  
});