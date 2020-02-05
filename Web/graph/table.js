(function (d3) {
    'use strict';

    const render = data => {

        var tr = d3.select(".objecttable tbody")
            .selectAll("tr")
            .data(data)
            .enter().append("tr")

        var td = tr.selectAll("td")
            .data(function(d, i) { return Object.values(d); })
            .enter().append("td")
                .text(function(d) { return d; });

    };

    d3.csv('https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/Donnees/clusters.csv')
        .then(data => {
            data.forEach(d => {

            });
            render(data);
        });
}(d3));