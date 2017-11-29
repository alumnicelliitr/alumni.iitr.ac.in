(function () {

	$('.message-button').on('click', function(){
		var alum_id = $(this).attr('data');
	  	$.ajax({
		    method:"POST",
		    url:'chat_request/',
		    data:{
		      "alumni_id":alum_id
		    },
		    success:function(res){
		    	if(res.done){
		    		$('#success').modal('show');
		    	}
		    }
	  	})
	})
})();