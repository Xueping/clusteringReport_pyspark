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
      .text(function(d) { return d.children ? 'Population: '+d.name +',\n\r Cluster: '+d.clusterId : 'RecordId: '+d.name +',\r\n Cluster: Leaf Node'; });


	var popup = d3.select('#popup')
		.style('width', w + 'px')
		.style('height', height_pie + 'px')
	
	d3.select('#pie_gender')
		.style('width', width_pie + 'px')
		.style('height', height_pie + 'px');
	
	var pie_gender = new d3pie('pie_gender', {
		header: {
			title: {
				text: 'Gender percentage',
				fontSize: 20
			}
		},
		size: {
		    'canvasWidth': height_pie,
			'canvasHeight': height_pie,
		    'pieInnerRadius': '50%',
		    'pieOuterRadius': '72%'
		},
		data: {
			content: [
				{ label: 'Male', value: root.gender.M },
				{ label: 'Female', value: root.gender.F }
			]
		}
	});
	
	d3.select('#pie_age')
		.style('width', width_pie + 'px')
		.style('height', height_pie + 'px');
		
	var pie_age = new d3pie('pie_age', {
		header: {
			title: {
				text: 'Age percentage',
				fontSize: 20
			}
		},
		size: {
		    'canvasWidth': height_pie,
			'canvasHeight': height_pie,
		    'pieInnerRadius': '50%',
		    'pieOuterRadius': '72%'
		},
		data: {
			content: [
				{ label: '<=12', value: root.adm.a1 },
				{ label: '50+', value: root.adm.a2 },
				{ label: '20~50', value: root.adm.a3 },
				{ label: '13~19', value: root.adm.a4 }
			]
		}
	});
	
	d3.select('#pie_freq')
		.style('width', width_pie + 'px')
		.style('height', height_pie + 'px');
		
	var pie_freq = new d3pie('pie_freq', {
		header: {
			title: {
				text: 'Frequence percentage',
				fontSize: 20
			}
		},
		size: {
		    'canvasWidth': height_pie,
			'canvasHeight': height_pie,
		    'pieInnerRadius': '50%',
		    'pieOuterRadius': '72%'
		},
		data: {
			content: [
				{ label: '11', value: root.payor.p1 },
				{ label: '12', value: root.payor.p2 },
				{ label: '13', value: root.payor.p3 },
				{ label: '14', value: root.payor.p4 },
				{ label: '15', value: root.payor.p5 },
				{ label: '16', value: root.payor.p6 },
				{ label: '17', value: root.payor.p7 },
				{ label: '18', value: root.payor.p8 }
			]
		}
	});

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

	
	var pieData = [];
	pieData.push({label: 'Male',value: d.gender.M});
	pieData.push({label: 'Female',value: d.gender.F});
    pie_gender.updateProp('data.content', pieData);
	
	var pieAgeData = [];
	pieAgeData.push({ label: '<=12',  value: d.adm.a1 });
	pieAgeData.push({ label: '50+',   value: d.adm.a2 });
	pieAgeData.push({ label: '20~50', value: d.adm.a3 });
	pieAgeData.push({ label: '13~19', value: d.adm.a4 });
	pie_age.updateProp('data.content', pieAgeData);
	
	var pieFreqData = [];
	pieFreqData.push({ label: '11', value: root.payor.p1 });
	pieFreqData.push({ label: '12', value: root.payor.p2 });
	pieFreqData.push({ label: '13', value: root.payor.p3 });
	pieFreqData.push({ label: '14', value: root.payor.p4 });
	pieFreqData.push({ label: '15', value: root.payor.p5 });
	pieFreqData.push({ label: '16', value: root.payor.p6 });
	pieFreqData.push({ label: '17', value: root.payor.p7 });
	pieFreqData.push({ label: '18', value: root.payor.p8 });
	pie_freq.updateProp('data.content', pieFreqData);
		
  }

  function transform(d) {
    return 'translate(8,' + d.dx * ky / 2 + ')';
  }