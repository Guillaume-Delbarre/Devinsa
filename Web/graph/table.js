(function (d3) {
    'use strict';

    var tabulate = function (data,columns) {
        var table = d3.select('body').append('table')
          var thead = table.append('thead')
          var tbody = table.append('tbody')
      
          thead.append('tr')
            .selectAll('th')
              .data(columns)
              .enter()
            .append('th')
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
      
        return table;
      }

    d3.csv('https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/Donnees/infoClusters.csv')
        .then(data => {
            
            var col = Object.keys(data)
            

            tabulate(data,col)
            console.log(data)
            console.log(col)
            console.log(Object.values(data))
        });
}(d3));