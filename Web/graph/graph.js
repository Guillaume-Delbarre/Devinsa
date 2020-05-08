var socket = io.connect('http://127.0.0.1:8080');

var svg = d3.select('#zoneGraph')

const widthTotal = +svg.attr('width');
const heighTotal = +svg.attr('height');

var margin = {top: 0, right: 0, bottom: 0, left: 0},
  width = widthTotal - margin.left - margin.right,
  height = heighTotal - margin.top - margin.bottom;

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

var shiftKey;

var rect,
node;

var div = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

svg = svg.append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var selection = [];
var selection1 = [];
var selection2 = [];
var nomSelectionne =[];

function attr_select1(){
  selection1 = [];
  node.each(function(d) {
    if (d.selected) {
       selection1.push(d.Name);
    }
  });
}

function attr_select2(){
  selection2 = [];
  node.each(function(d) {
    if (d.selected) {
       selection2.push(d.Name);
    }
  });
}

function aff_select1(){
  node.classed('selected', function (d) {
    if (selection1.includes(d.Name)){
      return d.selected = true;
    } else {
      return d.selected = false;
    }
  })
}

function aff_select2(){
  node.classed('selected', function (d) {
    if (selection2.includes(d.Name)){
      return d.selected = true;
    } else {
      return d.selected = false;
    }
  })
}

var clust;

function attr_clust_select1(){
  var i = 0;
  node.each(function(d) {
    if (d.selected) {
       i += 1;
       clust = d.Cluster;
    }
  });
  if (i<2) {
    node.each(function(d) {
      if (d.Cluster == clust) {
         selection1.push(d.Name);
      }
    });
    aff_select1();
  } else {
    window.alert("La sélection n'a pas marchée, veuillez ne sélectionner qu'un seul cluster");
  }
}

function attr_clust_select2(){
  var i = 0;
  node.each(function(d) {
    if (d.selected) {
       i += 1;
       clust = d.Cluster;
    }
  });
  if (i<2) {
    node.each(function(d) {
      if (d.Cluster == clust) {
         selection2.push(d.Name);
      }
    });
    aff_select2();
  } else {
    window.alert("La sélection n'a pas marchée, veuillez ne sélectionner qu'un seul cluster");
  }
}

function aff_nom_select1(){
  //window.alert(selection1)
  console.log(selection1)
}

function aff_nom_select2(){
  //window.alert(selection2)
  console.log(selection2)
}

function selection_to_nom(objSelect){
  var ret = [];
  for(var i=0;i<objSelect.length;i++){
    ret.push(objSelect[i].Name)
  }
  return ret;
}

function annuler_selection(){
  console.log('annuler')
  clear_selection();
  document.getElementById("tabButton").rows[0].cells[0].innerHTML = "<input type=\"button\" onclick=\"get_selection();\" value=\"Appliquer la selection\">"
  document.getElementById("tabButton").rows[1].cells[0].innerHTML = "<input type=\"button\" onclick=\"comp_selection_clust();\" value=\"Comparer la sélection à un groupe\">"
  document.getElementById("tabButton").rows[2].cells[0].innerHTML = "<input type=\"button\" onclick=\"comp_selection_select();\" value=\"Comparer la sélection à une autre sélection\">"
}

function comp_selection_clust(){
  selection = return_selection();
  clear_selection();
  console.log('select clust')
  document.getElementById("tabButton").rows[0].cells[0].innerHTML = "<input type=\"button\" onclick=\"annuler_selection();\" value=\"Annuler\">"
  document.getElementById("tabButton").rows[1].cells[0].innerHTML = "<p> Sélectionnez un personnage pour connaitre son cluster <p>"
  document.getElementById("tabButton").rows[2].cells[0].innerHTML = "<input type=\"button\" onclick=\"valider_cluster();\" value=\"Valider\">"
}

function valider_cluster(){
  selection2 = return_selection();
  if(selection2.length != 1){
    document.getElementById("tabButton").rows[1].cells[0].innerHTML = "<p> Sélectionnez un unique personnage <p>"
  } else {
    console.log("Selection de cluster")
    nomSel = selection_to_nom(selection);
    console.log(nomSel)
    console.log(selection2[0].Cluster)
    socket.emit('ecrirequestiondiff', ({liste1: nomSel, liste2: selection2[0].Cluster}));
      d3.csv("differences.csv", function(data) {
        //console.log(data)
        var t = $('#listQusetion').DataTable();
        t.clear().draw();
        for(let i = 0; i<data.length; i++){
          t.row.add([data[i].Question, data[i].Différences]).draw(false);
        }
    })
  }
}

function comp_selection_select(){
  selection = return_selection();
  clear_selection();
  console.log('select select')
  document.getElementById("tabButton").rows[0].cells[0].innerHTML = "<input type=\"button\" onclick=\"annuler_selection();\" value=\"Annuler\">"
  document.getElementById("tabButton").rows[1].cells[0].innerHTML = "<p> Faites une autre sélection <p>"
  document.getElementById("tabButton").rows[2].cells[0].innerHTML = "<input type=\"button\" onclick=\"valider_select();\" value=\"Valider\">"
}

var nomSel = [];
var nomSel2 = [];

function valider_select(){
  selection2 = return_selection();
  if(selection2.length > 1){
    nomSel = selection_to_nom(selection);
    nomSel2 = selection_to_nom(selection2);
    console.log(nomSel)
    console.log(nomSel2)
    //retourTableau = fontionListe();
    socket.emit('ecrirequestiondiff', ({liste1: nomSel, liste2: nomSel2}));
    d3.csv("differences.csv", function(data) {
      //console.log(data)
      var t = $('#listQusetion').DataTable();
      t.clear().draw();
      for(let i = 0; i<data.length; i++){
        t.row.add([data[i].Question, data[i].Différences]).draw(false);
	    }
    })
  }
}

$(document).ready( function () {
    $('#listQusetion').DataTable();
} );

function return_selection(){
  ret = [];
  node.each(function(d) {
    if (d.selected) {
       ret.push(d);
    }
  });
  return ret;
}

function get_selection(){
  selection = [];
  node.each(function(d) {
    if (d.selected) {
       selection.push(d);
    }
  });
  var nomsPerso = []
  nomSelectionne = []
  for(i=0;i<selection.length;i++){
    nomsPerso.push([selection[i].Name,selection[i].Cluster])
    nomSelectionne.push(selection[i].Name)
  }
  console.log(nomSelectionne)
}

function clear_selection() {
  node.classed('selected', function (d) { return d.selected = false; })
}

d3.csv("resPCA.csv", function(error, data) {
  data.forEach(function(d) {
    d.Axe_X = +d.Axe_X;
    d.Axe_Y = +d.Axe_Y;
    d.Medoid = +d.Medoid;
  });

  var nomAfficher = false;

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
        node.each(function(d) { d.previouslySelected = shiftKey && d.selected; });
        if (!shiftKey) {
          d3.event.target.clear();
          d3.select(this).call(d3.event.target);
        }
      })
      .on("brush", function() {
        if (shiftKey) {
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
        svg.call(d3.behavior.zoom().x(x).y(y).on("zoom", zoom));
      }));

  function zoom() {
    if (shiftKey) {
      console.log('zoom shiftKey');
      return;
    }
    node.attr("cx", function(d) { return x(d.Axe_X); })
      .attr("cy", function(d) { return y(d.Axe_Y); });
    if(nomAfficher){
      nomsTitre.attr('x', function(d) { return x(d.Axe_X); })
        .attr('y', function(d) { return y(d.Axe_Y) - 15; });
    }
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
      }
    })
    .on("mouseover", function(d) {
      div.transition()
          .duration(200)
          .style("opacity", .9);
      div	.html(d.Name)
          .style("left", (d3.event.pageX) + "px")
          .style("top", (d3.event.pageY - 21) + "px");
      })
    .on("mouseout", function(d) {
      div.transition()
          .duration(500)
          .style("opacity", 0);
    });

  function affiche_nom(){
    if(nomAfficher){
      nomsTitre.remove();
    } else {
      nomsTitre = svg.selectAll(".titrePerso")
      .data(data)
      .enter().append('text')
        .attr('class', 'titrePerso')
        .attr('font-size', '12px')
        .attr('stroke-width', '1px')
        .attr('text-anchor', 'middle')
        .attr('x', function(d) { return x(d.Axe_X); })
        .attr('y', function(d) { return (y(d.Axe_Y) - 15); })
        .text(function(d) { return d.Name })
    }
    
  }
  
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
