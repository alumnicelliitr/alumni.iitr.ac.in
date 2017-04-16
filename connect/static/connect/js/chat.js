'use strict';

(function() {

	var BASE = 'http://192.168.121.187:6969/connect/';

	function getChatUserList() {

		$.ajax({
		    method:"POST",
		    url: BASE + 'chat_user_list/',
		    data: {
				'enrollment_no' : enrollment_no
			},
		    success:function(res){
		    	console.log(res);
		    	if(res){
		    		var html = '';
		    		res.forEach(function(d, i){
						html += '<div class="alumni-name">' + 
									'<a class="alumni-name-chat" data="' + d.username +  '">' + d.name + '</a>' + 
								'</div>';
		    		})
					$('.chat-list').html(html);
		    	}
		    }
	  	});
	}

	function getChatUserHistory(alumni_id) {

		$.ajax({
		    method:"POST",
		    url: BASE + 'chat_list/',
		    data: {
				'student_id' : enrollment_no, 
				'alumni_id' : alumni_id
			},
		    success:function(res){
		    	console.log(res);
		    	if(res){
		    		var message = 'sdcscsdcsdcsd';
		    		var messages = '';
		    		[1,0,1,0].forEach( function(d, i){
		    			if(d){
		    				messages += '<div class="sent-message">'+ message + 
									'</div>';
		    			}
		    			else{
		    				messages += '<div class="received-message">'+ message + 
									'</div>'
		    			}
		    		})

		    		$('.chat-messages').html(messages);
		    	}
		    }
	  	});
		
	}
	$('#send-message-form').submit(function(e) {
		e.preventDefault();
		var message = $('#message-bar').val();
		$.ajax({
		    method:"POST",
		    url: '/connect/message/',
		    data: {
        'target' : enrollment_no,
        'message' : message
		   	},
		    success:function(res){
          if(res == 'success')
          {
	  	      $('#message-bar').val('');
            message = '<div class="sent-message">' + message + '</div>';
            $('.chat-messages').prepend(message);
          }
		    }
	  	});
	});

	$('.chat-list').on('click', '.alumni-name-chat', function(){
		var alumni_id = $(this).attr('data');
		getChatUserHistory(alumni_id);
	})
	getChatUserList();
})();
