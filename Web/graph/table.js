(function (d3) {
    'use strict';

    var couleur = d3.scaleOrdinal(d3.schemeCategory10)
        .domain(["Groupe 0","Groupe 1","Groupe 2","Groupe 3","Groupe 4","Groupe 5","Groupe 6","Groupe 7","Groupe 8","Groupe 9"])

    var tabulate = function (data,columns) {
        var table = d3.select('body').append('table')
          var thead = table.append('thead')
          var tbody = table.append('tbody')
      
          thead.append('tr')
            .selectAll('th')
              .data(columns)
              .enter()
            .append('th')
              .style('color', function(d) {return couleur(d)})
              .text(function (d) { return d })
      
          var rows = tbody.selectAll('tr')
              .data(data)
              .enter()
            .append('tr')
      
          var cells = rows.selectAll('td')
              .data(function(row) {
                  return columns.map(function (column) {
                      return { column: column, value: row[column] }
                })
            })
            .enter()
          .append('td')
            .text(function (d) { return d.value })
            .style('color', function(d) { 
              if( (d.value).includes('.') ){
                if( (d.value).includes('-') ){
                  return 'red'
                } else {
                  return 'green'
                }
              } else {
                return 'black'
              }
            })
      
        return table;
      }

    d3.csv('https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/Donnees/infoClusters.csv')
        .then(data => {
            
            tabulate(data,data.columns)
            
        });
}(d3));