var w = 1200,
    h = 400,
    x = d3.scale.linear().range([0, w]),
    y = d3.scale.linear().range([0, h]),
	width_pie = w/3,
	height_pie = 300;

var vis = d3.select('#body').append('div')
    .attr('class', 'chart')
    .style('width', w + 'px')
    .style('height', h + 'px')
  .append('svg:svg')
    .attr('width', w)
    .attr('height', h);
	

var partition = d3.layout.partition()
    .value(function(d) { return d.size; });

var root = JSON.parse(flare);
  var g = vis.selectAll('g')
      .data(partition.nodes(root))
    .enter().append('svg:g')
      .attr('transform', function(d) { return 'translate(' + x(d.y) + ',' + y(d.x) + ')'; })
	  .on('click', click);

  var kx = w / root.dx,
      ky = h / 1;
  var color = d3.scale.category20c();
  var c20 = d3.scale.category20();

  g.append('svg:rect')
      .attr('width', root.dy * kx)
      .attr('height', function(d) { return d.dx * ky; })
      .attr('class', function(d) { return d.children ? 'parent' : 'child'; })
	  .style('fill', function(d,i){return d.children ? c20(i) : '#aaa';} );

  g.append('svg:text')
      .attr('transform', transform)
      .attr('dy', '.35em')
      .style('opacity', function(d) { return d.dx * ky > 12 ? 1 : 0; })
      .text(function(d) { return d.children ? 'Population: '+d.name +',\n\r Cluster: '+d.clusterId : 'Population: '+d.name +',\n\r Cluster: '+d.clusterId +', Leaf Node'; });


  function click(d) {
    
    kx = (d.y ? w - 40 : w) / (1 - d.y);
    ky = h / d.dx;
    x.domain([d.y, 1]).range([d.y ? 40 : 0, w]);
    y.domain([d.x, d.x + d.dx]);

    var t = g.transition()
        .duration(d3.event.altKey ? 7500 : 750)
        .attr('transform', function(d) { return 'translate(' + x(d.y) + ',' + y(d.x) + ')'; });

    t.select('rect')
        .attr('width', d.dy * kx)
        .attr('height', function(d) { return d.dx * ky; });

    t.select('text')
        .attr('transform', transform)
        .style('opacity', function(d) { return d.dx * ky > 12 ? 1 : 0; });

    d3.event.stopPropagation();
		
  }

  function transform(d) {
    return 'translate(8,' + d.dx * ky / 2 + ')';
  }