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

var unpack_for_line = function(ticker,stock_info){
	var price_list = stock_info

	

	
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

price count date

var make_line_graph = function(ticker, stock_info){
	const price_list = [ticker].concat(stock_info[0])
	const count_list = ['Activity'].concat(stock_info[1])
	const orig_date_list = stock_info[2]
	const date_list = ['x'].concat(stock_info[2])
	const columns = [price_list,count_list, date_list]

	require(["d3", "c3"], function(d3, c3){
		var chart = c3.generate({
			bindto:'.graphArea',
    		data: {
        		x: 'x',
        		columns: columns,
        		axes:{
        			'Activity': 'y2'
        		}
    		},
    		axis: {
    			y:{
    				label: {
    					text: "Price (in $USD)",
    					position: 'outer-middle'
    				}
    			},

    			y2:{
    				show: true,
    				label: {
    					text: "Activity",
    					position: 'inner-middle'

    				}

    			},

    			x:{
    				type:'timeseries',
    				tick:{values : orig_date_list}



    			}

    		}
		});
	})
};


document.getElementById('tsla').addEventListener('click', function(e){
	e.preventDefault()

	console.log('clicked')

	make_line_graph('TSLA', tesla_info)

});
document.getElementById('ko').addEventListener('click', function(e){
	e.preventDefault()
	console.log('clicked')

	make_bar_graph('KO', coke_info)

});
document.getElementById('snap').addEventListener('click', function(e){
	e.preventDefault()
	console.log('clicked')

	make_line_graph('SNAP', snap_info)

});


