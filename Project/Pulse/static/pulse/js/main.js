var bulk_info = $.ajax(
		{
			url: 'http://127.0.0.1:8000/graph',
			method: 'GET',
			success: function(result){
				return result

			}
		}
)
 const tesla_info = bulk_info['result']['tesla']
 const coke_info = bulk_info['result']['coke']
 const snap_info = bulk_info['result']['snap']

var package_for_line = function(stock_info){
	
	

	
}



require.config({
			baseUrl: '/js',
			paths: {
    		d3: "http://d3js.org/d3.v3.min"
  			}
		});



// STATIC FUNCTIONS
var make_bar_graph = function(){
	require(["d3", "c3"], function(d3, c3) {

		var chart = c3.generate({
			bindto: '.graphArea',
	    	data: {
	        	columns: [
	            	['stock_price', 30, 200, 100, 400, 150, 250,1000],
	            	['news_artciles', 130, 100, 140, 200, 150, 50,1000],
	            	['tweets', 400, 150, 10, 20, 30, 40,1000],
	        	],
	        	type: 'bar'
	    	},
	   		bar: {
	        	width: {
	            	ratio: 0.3 // this makes bar width 50% of length between ticks
	        	}

	    	}
		});
	});

};


var make_line_graph = function(){
	require(["d3", "c3"], function(d3, c3){
		var chart = c3.generate({
			bindto:'.graphArea',
    		data: {
        		x: 'x',
        		columns: [
		            ['x', 20, 50, 100, 230, 300, 310],
		            ['data1', 30, 200, 100, 400, 150, 250],
		            ['data2', 130, 300, 200, 300, 250, 450]
        		]
    		}
		});
	})
};


document.getElementById('tsla').addEventListener('click', function(e){
	e.preventDefault()

	console.log('clicked')

	make_line_graph()

});
document.getElementById('ko').addEventListener('click', function(e){
	e.preventDefault()
	console.log('clicked')

	make_bar_graph()

});
document.getElementById('snap').addEventListener('click', function(e){
	e.preventDefault()
	console.log('clicked')

	make_line_graph()

});


