var color = d3.scale.category10();

function tabulate(data, columns) {
  var table = d3.select("body").append("table"),
      thead = table.append("thead"),
      tbody = table.append("tbody");

  // Append the header row
  thead.append("tr")
      .selectAll("th")
      .data(columns)
      .enter()
      .append("th")
        .style('color', function(d) { if(d.includes('Groupe')){
            return color(d)
        } else {
            return "black";
        }})
        .text(function(column) {
            return column;
        });

  // Create a row for each object in the data
  var rows = tbody.selectAll("tr")
      .data(data)
      .enter()
      .append("tr");

  // Create a cell in each row for each column
  var cells = rows.selectAll("td")
      .data(function(row) {
          return columns.map(function(column) {
              return {
                  column: column,
                  value: row[column]
              };
          });
      })
      .enter()
      .append("td")
          .text(function(d) { return d.value; })
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
          });

  return table;
}

d3.csv("https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/Donnees/infoClusters.csv", function(data) {
    //console.log(data[0])
    //console.log(data)
    tabulate(data,["Groupe 0","131 personnages","Groupe 1","567 personnages","Groupe 2","425 personnages","Groupe 3","307 personnages"])
})