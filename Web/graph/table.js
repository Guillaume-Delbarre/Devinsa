var color = d3.scale.category10();

function tabulate(donnee,columns){
  var table = d3.select("#tableResult").append("table");
  thead = table.append("thead");
  tbody = table.append('tbody');

  console.log('test');

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

  var tr = tbody.selectAll("tr")
    .data(donnee.filter(function(d,i){
      if(i>0){
        return d;
      }
    }))
    .enter()
    .append('tr');

  var td = tr.selectAll("td")
    .data(function(d) { return d; })
    .enter()
    .append('td')
    .text(function(d) {return d;})
    .style('color', function(d) { 
      if( (d).includes('.') ){
        if( (d).includes('-') ){
          return 'red'
        } else {
          return 'green'
        }
      } else {
        return 'black'
      }});
}

function miseEnPage(data) {
  var tab = [];
  for(var i = 0;i < data.length; i++){
    tab.push(Object.values(data[i]));
  }
  return tab;
}

d3.csv("https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/Donnees/infoClusters.csv", function(data) {
    //console.log(Object.values(data[0]))
    tableau = miseEnPage(data)
    console.log(tableau)
    tabulate(tableau,tableau[0])
})