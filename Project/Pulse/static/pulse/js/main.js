// var tesla_info=[];
// var coke_info=[]; 
// var snap_info=[]; 
var tesla_info; 
var coke_info;
var snap_info;

var data;
var bulk_info = $.ajax(
		{
			url: 'http://127.0.0.1:8000/graph',
			method: 'GET',
			success: function(result){
				data = JSON.parse(result);
				// console.log('data')
				// console.log(data)
				$('.loader').css('display','none')
				tesla_info = data['result']['tesla']
				coke_info = data['result']['coke']
				snap_info = data['result']['snap']
				// return data
			}
		}
)


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

var make_bar_graph = function(stock_info){
	console.log("making BAR graph")
	const stock_data = stock_info[0]
	const ticker = stock_info[0]['company']
	const count_list = ['Activity'].concat(stock_info[1])
	const price_list = [ticker].concat(stock_data['price_list'])
	const date_list = ['x'].concat(stock_info[2])

	require(["d3", "c3"], function(d3, c3) {

		var chart = c3.generate({
			bindto: '.graphArea',
	    	data: {

	        	columns: [
	            		// date_list,
	            		price_list,
        				count_list
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

var make_line_graph = function(stock_info){
	console.log("making LINE graph")
	const stock_data = stock_info[0]
	console.log(stock_info)
	const ticker = stock_info[0]['company']
	const price_list = [ticker].concat(stock_data['price_list'])
	console.log(price_list)
	const count_list = ['Activity'].concat(stock_info[1])
	const orig_date_list = stock_info[2]
	const date_list = ['x'].concat(stock_info[2])
	// const columns = [price_list,count_list, date_list]

	require(["d3", "c3"], function(d3, c3){
		var chart = c3.generate({
			bindto:'.graphArea',
    		data: {
        		x: 'x',
        		columns: [date_list,
        				price_list,
        				count_list
        		],
        		axes:{
        			'Activity': 'y2'
        		},
        		onclick: function(e){side_bar(e)}
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
	$('.graphButton').val('Bar');
	$('#loadingMessage').css('display', 'none')
	console.log('clicked')
	var tesla = $(this)
	tesla.addClass('active')
	$('#ko').removeClass('active')
	$('#snap').removeClass('active')
	make_line_graph(tesla_info)

});

$('#ko').on('click', function(e){
	$('.graphButton').val('Bar');
	$('#loadingMessage').css('display', 'none')
	console.log('clicked')
	$(this).addClass('active')
	$('#snap').removeClass('active')
	$('#tsla').removeClass('active')
	make_line_graph(coke_info)

});

$('#snap').on('click', function(e){
	$('.graphButton').val('Bar');
	$('#loadingMessage').css('display', 'none')
	console.log('clicked')
	$(this).addClass('active')
	$('#ko').removeClass('active')
	$('#tsla').removeClass('active')
	make_line_graph(snap_info)
	
	
	// make_bar_graph('SNAP', snap_info)
	
	

});

$('.graphButton').on('click', function(){
	// console.log(this.value)
	var graphArea =$('.graphArea'); 
	if (this.value == 'Bar'){
		this.value = 'Line'
		graphArea.empty()
		var info=check()
		make_bar_graph(info)	

	}

	else if(this.value == 'Line'){
		this.value = 'Bar'
		graphArea.empty()
		var info=check()
		make_line_graph(info)
		
	}
	else{
		this.value = "Damn it Wes!"

	}




});

var check = function(){
	var active=$('.active');
	// console.log('[[[[[[[[[[[[[[[[[[[[active.id')
	// console.log(active[0].id)

	if (active[0].id=='tsla'){
		return tesla_info
	}
	else if (active[0].id=='ko'){
		return coke_info
	}
	else{
		return snap_info
	}
}

var side_bar=function(e){
	console.log(e.x)
	// console.log(this)
}