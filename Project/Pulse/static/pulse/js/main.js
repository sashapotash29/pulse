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
// CODE FROM RESOURCE
var doc = new jsPDF();
var specialElementHandlers = {
    '#editor': function (element, renderer) {
        return true;
    }
};

$('#saveButton').on('click', function(){
	console.log("Save has been clicked")
	var picture = $('.middle')
	var dataURL = picture.toDataURL();
	var doc = new jsPDF();
	console.log('here')
	// var specialElementHandlers = {
 //    	'#editor': function (element, renderer) {
 //        return true;
 //    	}
	// };
	console.log('here')
	doc.fromHTML($('.graphArea').html(), 15, 15, {
		width: 200,
		'elementHandlers': specialElementHandlers
	});
	doc.addImage(dataURL,'JPEG',0,0)
	doc.save('PulseSample.pdf');

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
	
	var company = $('.active')[0].id
	var date= e.x
	console.log(company)
	console.log(date)
	console.log(this)
	$('.newsLoader').css('display','block')
	$('.tweetsLoader').css('display','block')
	$.ajax(
		{
			url: 'http://127.0.0.1:8000/media/'+company+'&'+date,
			method: 'GET',
			success: function(result){
				$('.newsLoader').css('display','none')
				data = JSON.parse(result);
				const news_ul = $('.newsInfo')
				const news = data['news']
				for(i=0; i++; i <= news.length){
					const news_li = $('<li>')
					news_li.addClass('newsLi')
					// TARGET THE CONTENT NOT EVERYTHING
					const content = news[i]
					const author = news[i]
					news_li.append(content + ' written by: ' + author)
					const linkTag = $('<a>')
					// WHERE IS THE LINK IN THE OBJ
					const link = news[i]
					linkTag.attr('href', link)
					linkTag.attr('value', 'Link to Tweet')
					linkTag.attr('target', '_blank')
					news_li.append(linkTag)
					news_ul.append(news_li)
	
				}
				// FIRST 'FOR LOOP' FOR NEWS ENDS
				$('.tweetsLoader').css('display','none')
				const professional_ul = $('.professionalsInfo')
				const tweets = data['tweets']
				for (i=0; i++; i <= tweets.length){
					const tweets_li = $('<li>')
					tweets_li.addClass('tweetsLi')
					// TARGET THE CONTENT NOT EVERYTHING?
					const content = tweets[i]
					const author = tweets[i]
					tweets_li.append(content + ' written by: ' + author)
					const linkTag = $('<a>')
					// WHERE IS THE LINK IN THE OBJ?
					const link = tweets[i]
					linkTag.attr('href', link)
					linkTag.attr('value', 'Link to News Article')
					linkTag.attr('target', '_blank')
					tweets_li.append(linkTag)
					professional_ul.append(tweets_li)
				}
				// SECOND 'FOR LOOP' FOR TWEETS ENDS
			}

		}
		}
	
	)

};




var bulk_info = $.ajax(
		{
			url: 'http://127.0.0.1:8000/graph',
			method: 'GET',
			success: function(result){
				$('.loader').css('display','none')
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
