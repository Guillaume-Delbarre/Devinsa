var margin = {top: 0, right: 0, bottom: 0, left: 0},
  width = 800 - margin.left - margin.right,
  height = 450 - margin.top - margin.bottom;

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
  .attr("class", "zone")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom);

var shiftKey;

var rect, 
node;

svg = svg.append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var selection = [];

function tabulatePerso(array){
  table = document.getElementById("tableSelect");
  for(var i = 0; i < array.length; i++){
    var newRow = table.insertRow(-1);
    for(var j = 0; j < array[i].length; j++){
      var newCell = newRow.insertCell(j);
      let newText = document.createTextNode(array[i][j]);
      newCell.appendChild(newText)
      console.log(array[i][j])
    }
  }
}

function get_selection(){
  selection = [];
  node.each(function(d) {
    if (d.selected) {
       selection.push(d);
    }
  });
  console.log(selection);
  var nomsPerso = []
  var tabletemp = document.getElementById("tableSelect");
  tabletemp.innerHTML = "<thead><tr><th>Personnage sélectionné</th><th>Cluster</th></tr></thead>";
  for(i=0;i<selection.length;i++){
    nomsPerso.push([selection[i].Name,selection[i].Cluster])
  }
  console.log(nomsPerso)
  tabulatePerso(nomsPerso)
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

  var brush = svg.append("g")
    .datum(function() { return {selected: false, previouslySelected: false}; })
    .attr("class", "brush")
    .call(d3.svg.brush()
      .x(d3.scale.identity().domain([0, width]))
      .y(d3.scale.identity().domain([0, height]))
      .on("brushstart", function(d) {
        svg = svg.call(d3.behavior.zoom().on("zoom", null));
        //console.log('brushstart');
        node.each(function(d) { d.previouslySelected = shiftKey && d.selected; });
        if (!shiftKey) {
          d3.event.target.clear();
          d3.select(this).call(d3.event.target);
        }
      })
      .on("brush", function() {
        if (shiftKey) {
          //console.log('shiftKey', shiftKey);
          var extent = d3.event.target.extent();
          //console.log(extent)
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
        svg.call(d3.behavior.zoom().x(x).y(y).on("zoom", zoom));
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
    .attr("r", function(d) { if(d.selected){return 7} else {return 5} })
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
        document.getElementById('persoSelectionne').innerText = d.Name
      }
    });

  var circleTitle = svg.selectAll('text').data(data)
    .enter().append('text')
      .attr('clip-path', 'url(#rect-clip)')
      .attr('class', 'circleTitle')
      .attr('opacity', 0)
      .attr('stroke', 'black')
      .attr('stroke-width', d => 1.5*d.Medoid)
      .attr('x', d => x(d.Axe_X))
      .attr('y', d => y(d.Axe_Y) + 12)
      .text(d => d.Name)

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