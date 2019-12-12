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
svg.append("g") //Ajout de l'axe au svg
    .attr("transform", "translate(0," + height + ")") //Décalage de l'axe des X vers le bas
    .call(d3.axisBottom(x));

var y = d3.scaleLinear()
    .domain([-12, 14])
    .range([ height, 0]);
svg.append("g")
    .call(d3.axisLeft(y));

var div = d3.select("body").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0);

// Ajout des points
var myCircle = svg.append('g')
    .selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", function (d) { return x(d.Axe_X); } )
    .attr("cy", function (d) { return y(d.Axe_Y); } )
    .attr("r", 8)
    .style("fill", "#440154ff" )
    .style("opacity", 0.5)
    .on("mouseover", function(d) {
        div.transition()
            .duration(200)
            .style("opacity", .9);
        div.html("Nom : " + d.Name)
            .style("left", (d3.event.pageX + 30) + "px")
            .style("top", (d3.event.pageY - 30) + "px")
    })
    .on("mouseout", function(d) {
        div.style("opacity", 0);
        div.html("")
            .style("left", "-500px")
            .style("top", "-500px");
    });

/*
// Zone de Sélection
svg
    .call( d3.brush()                 // Ajout de la fonction d3.brush fonction de sélection
    .extent( [ [0,0], [width,height] ] ) // Initialise la zone possible de sélection
    .on("start brush", updateChart) // Déclanche la fonction 'updateChart' à chaque fois que la sélection change
    ) // Possibilité de bouger la zone de sélection

// Fonction appélé par la sélection
function updateChart() {
    extent = d3.event.selection
    myCircle.classed("selected", function(d){ return isBrushed(extent, x(d.Axe_X), y(d.Axe_Y) ) } )
}

// Fonction qui retourne True si le point est dans la sélection
function isBrushed(brush_coords, cx, cy) {
    var x0 = brush_coords[0][0],
        x1 = brush_coords[1][0],
        y0 = brush_coords[0][1],
        y1 = brush_coords[1][1];
    return x0 <= cx && cx <= x1 && y0 <= cy && cy <= y1;
}
*/
})
