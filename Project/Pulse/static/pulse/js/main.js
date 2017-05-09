// var tesla_info=[];
// var coke_info=[]; 
// var snap_info=[]; 
var tesla_info; 
var coke_info;
var snap_info;
console.log("PULSE STATIC FILE")
var data;
var bulk_info = $.ajax(
		{
			url: '/graph',
			// url: 'http://127.0.0.1:8000/graph',
			// url: 'http://www.checkthepulse.today/graph',
			method: 'GET',
			success: function(result){
				data = JSON.parse(result);
				console.log('success?')
				// console.log(data)
				$('.loader').css('display','none')
				$('#loadingMessage').toggleClass('showing')
				tesla_info = data['result']['tesla']
				coke_info = data['result']['coke']
				snap_info = data['result']['snap']
				// return data
			}
		}
)




// var unpack_for_line = function(ticker,stock_info){
// 	var price_list = stock_info

	

	
// }



require.config({
			baseUrl: '/js',
			paths: {
    		d3: "http://d3js.org/d3.v3.min"
  			}
		});



// STATIC FUNCTIONS

var make_bar_graph = function(stock_info){
	console.log("making BAR graph")
	var stock_data = stock_info[0]
	var ticker = stock_info[0]['company']
	var count_list = ['Activity'].concat(stock_info[1])
	var price_list = [ticker].concat(stock_data['price_list'])
	var orig_date_list = stock_info[2]
	var date_list = ['x'].concat(stock_info[2])
	console.log(date_list)
	require(["d3", "c3"], function(d3, c3) {

		var chart = c3.generate({
			bindto: '.graphArea',
	    	data: {
				x: 'x',
        		columns: [date_list,
        				price_list,
        				count_list
        		],
        		axes:{
        			'Activity': 'y2'
        		},
	        	type: 'bar',
	        	onclick: function(e){side_bar(e)}
	    	},
	   		bar: {
	        	width: {
	            	ratio: 0.3 // this makes bar width 50% of length between ticks
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
    					position: 'outer-middle'

    				}

    			},

    			x:{
    				type:'timeseries',
    				tick:{values : orig_date_list}



    			}

    		}
		});
	});

};

// price count date

var make_line_graph = function(stock_info){
	// console.log("making LINE graph")
	var stock_data = stock_info[0]
	// console.log(stock_info)
	var ticker = stock_info[0]['company']
	var price_list = [ticker].concat(stock_data['price_list'])
	console.log(price_list)
	var count_list = ['Activity'].concat(stock_info[1])
	var orig_date_list = stock_info[2]
	var date_list = ['x'].concat(stock_info[2])
	// var columns = [price_list,count_list, date_list]

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
    					position: 'outer-middle'

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
	// console.log('clicked')
	$('.middleTop').css('display','block')
	$('.graphTitle h1').text(this.value)
	var tesla = $(this)
	tesla.addClass('active')
	$('#ko').removeClass('active')
	$('#snap').removeClass('active')
	make_line_graph(tesla_info)

});

$('#ko').on('click', function(e){
	$('.graphButton').val('Bar');
	$('#loadingMessage').css('display', 'none')
	// console.log('clicked')
	$('.graphTitle h1').text(this.value)
	$('.middleTop').css('display','block')
	$(this).addClass('active')
	$('#snap').removeClass('active')
	$('#tsla').removeClass('active')
	make_line_graph(coke_info)

});

$('#snap').on('click', function(e){
	$('.graphButton').val('Bar');
	$('#loadingMessage').css('display', 'none')
	// console.log('clicked')
	$('.graphTitle h1').text(this.value)
	$('.middleTop').css('display','block')
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
// http://www.checkthepulse.today
var side_bar=function(e){
	
	var company = $('.active')[0].id
	var date= e.x
	console.log(company)
	console.log(date)
	// console.log(this)
	$('.newsLoader').css('display','block')
	$('.tweetsLoader').css('display','block')
	$.ajax(
		{
			url: '/media',
			// url: 'http://127.0.0.1:8000/media',
			// url: 'http://www.checkthepulse.today/media',
			data: {'company':company, 'date':date},
			method: 'GET',
			// dataType: 'application/json',
			success: function(result){
				$('.newsLoader').css('display','none')
				$('.tweetsLoader').css('display','none')
				data = JSON.parse(result);
				console.log('....................data')
				console.log(data)
				var news_ul = $('.newsInfo');
				news_ul.empty()
				var news = data['news'];
				console.log('news');
				if (news.length == 0){
					var news_li = $('<li>Sorry no News Activity for this Day</li>')
					news_li.addClass('tweetsLi')
					// TARGET THE CONTENT NOT EVERYTHING?
					news_ul.append(news_li)
				}
				else{
					for(var i=0; i <= news.length-1;i++){
						
						console.log('forloop news')
						var news_li = $('<li></li>')
						news_li.addClass('newsLi')
						// TARGET THE CONTENT NOT EVERYTHING
						var content = news[i]['title']
						console.log(content)
						var author = news[i]['author']
						console.log(author)
						var linkTag = $('<a></a>')
						var p_tag = $('<p></p>')
						p_tag.append('written by: ' + author)
						linkTag.append(content)
						// WHERE IS THE LINK IN THE OBJ
						var link = news[i]['link']
						linkTag.attr('href', link)
						linkTag.attr('value', 'Link to Tweet')
						linkTag.attr('target', '_blank')
						news_li.append(linkTag)
						news_li.append(p_tag)
						news_ul.append(news_li)
		
					}
				}
				// FIRST 'FOR LOOP' FOR NEWS ENDS
				
				var professional_ul = $('.professionalsInfo')
				professional_ul.empty()
				var tweets = data['tweets']
				if (tweets.length == 0){
					var tweets_li = $('<li></li>')
					tweets_li.text('Sorry No Tweets Available For This Day')
					tweets_li.addClass('tweetsLi')

					// TARGET THE CONTENT NOT EVERYTHING?
					
					// tweets_li.append(linkTag)
					professional_ul.append(tweets_li)
				}
				else{
					for (i=0; i <= tweets.length-1; i++){
						var tweets_li = $('<li></li>')
						tweets_li.addClass('tweetsLi')
						// TARGET THE CONTENT NOT EVERYTHING?
						var content = tweets[i]['content']
						var author = tweets[i]['author']
						var linkTag = $('<a></a>')
						var p_tag = $('<p></p>')
						p_tag.append('written by: ' + author)
						linkTag.append(content)
						
						var link = tweets[i]['link']
						linkTag.attr('href', link)
						linkTag.attr('value', 'Link to News Article')
						linkTag.attr('target', '_blank')
						tweets_li.append(linkTag)
						tweets_li.append(p_tag)
						professional_ul.append(tweets_li)
					}
				}
				// SECOND 'FOR LOOP' FOR TWEETS ENDS
				var peep_ul = $('.PeoplesInfo');
				peep_ul.empty();
				var peep_tweets_li = $('<li></li>')
				peep_tweets_li.text('Sorry No Tweets Available For This Day');
				peep_ul.addClass('peepTweetsLi');
				peep_ul.append(peep_tweets_li);
			}

		}
	)
};
