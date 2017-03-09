// var tesla_info=[];
// var coke_info=[]; 
// var snap_info=[]; 
var tesla_info; 
var coke_info;
var snap_info;

var data;
// var bulk_info = $.ajax(
// 		{
// 			url: 'http://127.0.0.1:8000/graph',
// 			method: 'GET',
// 			success: function(result){
// 				data = JSON.parse(result);
// 				// console.log('data')
// 				// console.log(data)
// 				$('.loader').css('display','none')
// 				tesla_info = data['result']['tesla']
// 				coke_info = data['result']['coke']
// 				snap_info = data['result']['snap']
// 				// return data
// 			}
// 		}
// )


// console.log(tesla_info)
// function sleep(miliseconds) {
//    var currentTime = new Date().getTime();

//    while (currentTime + miliseconds >= new Date().getTime()) {
//    }
// }

// console.log('data');
// console.log(data);


// sleep(5000)
// console.log('bulk_info')
// console.log(bulk_info.responseText)




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
	console.log("making BAR graph")
	require(["d3", "c3"], function(d3, c3) {

		var chart = c3.generate({
			bindto: '.barGraph',
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

// price count date

var make_line_graph = function(ticker, stock_info){
	console.log("making LINE graph")
	const stock_data = stock_info[0]
	console.log(stock_data)
	const price_list = [ticker].concat(stock_data['price_list'])
	console.log(price_list)
	const count_list = ['Activity'].concat(stock_info[1])
	const orig_date_list = stock_info[2]
	const date_list = ['x'].concat(stock_info[2])
	// const columns = [price_list,count_list, date_list]

	require(["d3", "c3"], function(d3, c3){
		var chart = c3.generate({
			bindto:'.lineGraph',
    		data: {
        		x: 'x',
        		columns: [date_list,
        				price_list,
        				count_list
        				],
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


// ADDING EVENT LISTENERS


$('#tsla').on('click', function(){
	$('#loadingMessage').css('display', 'none')
	console.log('clicked')

	make_line_graph('TSLA', tesla_info)

});

$('#ko').on('click', function(e){
	$('#loadingMessage').css('display', 'none')
	console.log('clicked')

	make_line_graph('KO', coke_info)

});

$('#snap').on('click', function(e){
	$('#loadingMessage').css('display', 'none')
	console.log('clicked')

	
	make_line_graph('SNAP', snap_info)
	
	
	make_bar_graph('SNAP', snap_info)
	
	

});

$('.graphButton').on('click', function(){
	console.log(this.value)

	if (this.value == 'Bar'){
		this.value = 'Line'
		$('.barGraph').css('display','block')
		$('.lineGraph').css('display','none')
	}

	else if(this.value == 'Line'){
		this.value = 'Bar'
		$('.lineGraph').css('display','block')
		$('.barGraph').css('display','none')
	}
	else{
		this.value = "Damn it Wes!"

	}




});



