(function (d3) {
  'use strict';
  
  const svg = d3.select('svg');

  const width = +svg.attr('width');
  const height = +svg.attr('height');
  
  const render = data => {

    const button = svg.append('button')
    	.attr('class', 'button')
    
    const xValue = d => d.Axe_X;
    
    const yValue = d => d.Axe_Y;
    
    const circleRadius = 8;

    var clicked;
    var clickedCluster;
    
    const margin = { top: 60, right: 40, bottom: 88, left: 100 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    
    const xScale = d3.scaleLinear()
      .domain(d3.extent(data, xValue))
      .range([0, innerWidth])
      .nice();
    
    const yScale = d3.scaleLinear()
      .domain(d3.extent(data, yValue))
      .range([innerHeight, 0])
      .nice();
    
    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    const xAxis = d3.axisBottom(xScale)
      .tickSize(-innerHeight)
      .tickPadding(15);
    
    const yAxis = d3.axisLeft(yScale)
      .tickSize(-innerWidth)
      .tickPadding(10);
    
    const yAxisG = g.append('g').call(yAxis);
    
    const xAxisG = g.append('g').call(xAxis)
      .attr('transform', `translate(0,${innerHeight})`);
    
    xAxisG.select('.domain').remove();
    
    var zoom = d3.zoom()
    	.scaleExtent([.5,20])
    	.extent([[0,0], [innerWidth,innerHeight]])
    	.on('zoom', updateZoom);
    
    g.append('rect')
    	.attr('class', 'zoomRect')
    	.attr('width', innerWidth)
    	.attr('height', innerHeight)
    	.call(zoom);
    
    g.append('clipPath')
    	.attr('id', 'rect-clip')
    .append('rect')
    	.attr('width', innerWidth)
      .attr('height', innerHeight);
      
      var couleur = d3.scaleOrdinal(d3.schemeCategory10)
        .domain(["Groupe 0","Groupe 1","Groupe 2","Groupe 3","Groupe 4","Groupe 5","Groupe 6","Groupe 7","Groupe 8","Groupe 9"])
    
    var cercle = g.selectAll('circle').data(data)
                  .enter()
    cercle
      .append('circle')
        .attr('id', d => (d.Cluster).replace('Groupe ', ''))
    		.attr('clip-path', 'url(#rect-clip)')
    		.attr('class', 'myCircle')
        .attr('cy', d => yScale(yValue(d)))
        .attr('cx', d => xScale(xValue(d)))
        .attr('fill', d => couleur(d.Cluster))
        .attr('r', circleRadius)
        .attr('stroke', 'black')
        .attr('stroke-width', 0)
        .on("mousedown", clicked)
    	.append('title')
    		.text(d => d.Name);
    
    var circleTitle = g.selectAll('text').data(data)
      .enter().append('text')
      	.attr('clip-path', 'url(#rect-clip)')
      	.attr('class', 'circleTitle')
        .attr('opacity', 0)
        .attr('stroke', 'black')
        .attr('stroke-width', d => 1.5*d.Medoid)
      	.attr('x', d => xScale(xValue(d)))
      	.attr('y', d => yScale(yValue(d)) + circleRadius + 12)
    		.text(d => d.Name)
    
    function clicked(d) {

      if ( d3.event.button == 0) {

        if(clicked !== d.Name) {
          d3.selectAll('.active')
            .attr('class', 'myCircle');
          clicked = d.Name;
          d3.select(this)
            .attr('class', 'active');
          document.getElementById('tags').value = clicked;
          namepers = clicked;
        } else {
          d3.selectAll('.active')
            .attr('class', 'myCircle');
          clicked = null
          document.getElementById('tags').value = "";
          namepers = "";
        }

        var myTable = document.getElementById('tableSelect');
        myTable.rows[1].cells[1].innerHTML = clicked;

      } else if( d3.event.button == 2){

        if (clickedCluster !== d.Cluster) {
          d3.selectAll('.active')
            .attr('class', 'oldActive');
          d3.selectAll('.activeCluster')
            .attr('class', 'myCircle');
          clickedCluster = d.Cluster;
          d3.selectAll('#\\3'+ (d.Cluster).replace('Groupe ', ''))
            .attr('class', 'activeCluster');
          d3.selectAll('.oldActive')
            .attr('class', 'active');
        } else {
          d3.selectAll('.active')
            .attr('class', 'oldActive');
          d3.selectAll('.activeCluster')
            .attr('class', 'myCircle');
          d3.selectAll('.oldActive')
            .attr('class', 'active')
          clickedCluster = null

        }

        var myTable = document.getElementById('tableSelect');
        myTable.rows[1].cells[0].innerHTML = clickedCluster;

      }

    }

    function updateZoom() {

        var newX = d3.event.transform.rescaleX(xScale);
        var newY = d3.event.transform.rescaleY(yScale);
        
        var newXAxis = d3.axisBottom(newX)
          .tickSize(-innerHeight)
          .tickPadding(15);
        
        const newYAxis = d3.axisLeft(newY)
          .tickSize(-innerWidth)
          .tickPadding(10);
        
        xAxisG.call(newXAxis);
        yAxisG.call(newYAxis);

        g.selectAll('circle')
          .attr("cx", function(d) {return newX(d.Axe_X)})
          .attr("cy", function(d) {return newY(d.Axe_Y)});
        
        circleTitle
          .attr('x', d => newX(xValue(d)))
          .attr('y', d => newY(yValue(d)) + circleRadius + 12)
     
    }
    
    d3.selectAll('.toggle').on('change', function(d){
      var opa = +this.value
      afficheNoms(opa);
    });
    
    function afficheNoms(opacity) {
      circleTitle
      	.attr('opacity', opacity);
    }
  
  };
  
  d3.csv('https://raw.githubusercontent.com/Guillaume-Delbarre/Devinsa/master/Donnees/resPCA.csv')
  	.then(data => {
    	data.forEach(d => {
        d.Axe_X = +d.Axe_X;
        d.Axe_Y = +d.Axe_Y;
        d.Medoid = +d.Medoid;
      });
    	render(data);
  });
}(d3));