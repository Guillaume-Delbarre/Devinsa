(function (d3) {
    'use strict';

    const render = data => {

        var couleur = d3.scaleOrdinal(d3.schemeCategory10)
        .domain(["Groupe 0","Groupe 1","Groupe 2","Groupe 3","Groupe 4","Groupe 5","Groupe 6","Groupe 7","Groupe 8","Groupe 9"])

        var tr = d3.select(".objecttable tbody")
            .selectAll("tr")
            .data(data)
            .enter().append("tr")

        var td = tr.selectAll("td")
            .data(function(d, i) { return Object.values(d); })
            .enter().append("td")
                .text(function(d) { return d; })
                    .attr('fontcolor', d => couleur("Groupe " + d.Cluster));

    };

    d3.csv('https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/Donnees/infoClusters.csv')
        .then(data => {
            data.forEach(d => {

            });
            render(data);
        });
}(d3));