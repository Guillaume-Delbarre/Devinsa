var largeur = 760;
var hauteur = 700;

// dimensions et marges du graph
var marge = {haut: 10, droite: 30, bas: 30, gauche: 60},
    width = largeur - marge.gauche - marge.droite,
    height = hauteur - marge.haut - marge.bas;

// gestion de la taille de l'emplacement 'svg'
var svg = d3.select("#zone_graphique") //variable pour appeller l'objet svg
    .append("svg")
        .attr("width", largeur)
        .attr("height", hauteur)
    .append("g")
        .attr("transform", "translate(" + marge.gauche + "," + marge.haut + ")"); // déplacement du graph pour laisser une marge en haut et à gauche

//Récupération des données
d3.csv("https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/resPCA.csv", function(data) {

// Ajout des axes
var x = d3.scaleLinear()
    .domain([-8, 17]) //Les limites de l'axes (valeur)
    .range([ 0, width ]); //Les limites spaciales de l'axes (coordonnées)
var xAxis = svg.append("g") //Ajout de l'axe au svg
    .attr("transform", "translate(0," + height + ")") //Décalage de l'axe des X vers le bas
    .call(d3.axisBottom(x));

var y = d3.scaleLinear()
    .domain([-12, 14])
    .range([ height, 0]);
var yAxis = svg.append("g")
    .call(d3.axisLeft(y));

var clip = svg.append("defs").append("svg:clipPath")
    .attr("id", "clip")
    .append("svg:rect")
        .attr("width", width)
        .attr("height", height)
        .attr("x", 0)
        .attr("y", 0);

var scatter = svg.append("g")
    .attr("clip-path", "url(#clip)")

// Ajout des points
//var myCircle =
scatter //svg.append('g')
    .selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
        .attr("cx", function (d) { return x(d.Axe_X); } )
        .attr("cy", function (d) { return y(d.Axe_Y); } )
        .attr("r", 8)
        .style("fill", "#440154ff" )
        .style("opacity", 0.5)

var textBox = scatter
    .selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
        .attr("width", 150)
        .attr("height", 75)
        .attr("x", function (d) { return x(d.Axe_X) + 16} )
        .attr("y", function (d) { return y(d.Axe_Y) - 10; } )
        .attr("opacity", 0.5)

scatter
    .selectAll("text")
    .data(data)
    .enter()
    .append("text")
        .attr("x", function (d) { return x(d.Axe_X) + 16; } )
        .attr("y", function (d) { return y(d.Axe_Y) + 6; } )
        .text(function (d) { return d.Name } )
        .attr("font-family", "sans-serif")
        .attr("font-size", "20px")
        .attr("fill", "red")

var zoom = d3.zoom()
    .scaleExtent([.5, 20])
    .extent([[0, 0], [width,height]])
    .on("zoom", updateChart);

svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all")
    .attr("transform", "translate(" + marge.gauche + "," + marge.haut + ")")
    .call(zoom);

function updateChart() {

    var newX = d3.event.transform.rescaleX(x);
    var newY = d3.event.transform.rescaleY(y);

    xAxis.call(d3.axisBottom(newX))
    yAxis.call(d3.axisLeft(newY))

    scatter
        .selectAll("circle")
        .attr("cx", function(d) {return newX(d.Axe_X)})
        .attr("cy", function(d) {return newY(d.Axe_Y)});

    scatter
        .selectAll("text")
        .attr("x", function(d) {return newX(d.Axe_X) + 16})
        .attr("y", function(d) {return newY(d.Axe_Y) + 6});

    scatter
        .selectAll("rect")
        .attr("x", function(d) {return newX(d.Axe_X) + 16})
        .attr("y", function(d) {return newY(d.Axe_Y) - 10});
}
})
