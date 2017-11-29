$(document).ready(function(){
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var divx = document.getElementById("message-container-box");
	divx.scrollTop = divx.scrollHeight;
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
        headers: {
           "X-CSRFToken": getCookie("csrftoken")
        }
    });
    var n = window.location.href.split("/").length;
    var username = window.location.href.split("/")[n-2];
    JSON.stringify(username);
    var user = {'username':username};

	$('#message_form').submit(function(e){
		if($('#message').val() != 0){
			e.preventDefault();
			$.ajax({
				url: "/samp/add_message/",
				method:"POST",
				data: $(this).serialize(),
				success: function(result){
					message = document.getElementById('message').value;
					document.getElementById('message').value = '';
					content = '<div class="message message-right">\
							<div class="message-text-container">\
								'+message+'\
							</div>\
							</div>';
					element = document.getElementsByClassName('message-wrapper')[0];
					element.innerHTML = element.innerHTML + content;
					var divx = document.getElementById("message-container-box");
					divx.scrollTop = divx.scrollHeight;
				},
			});
		}
		else{
			e.preventDefault();
			alert("Please don't send empty messages!");
		}
	});

	var timeout = 5000;
	(function worker() {
	  $.get('/samp/pooling/', function(data) {
		var obj = JSON.parse(data)['unread_messages'];
		username = document.getElementById('username').value;
		if(obj[username].length > 0)
		{
			for(i=0;i<obj[username].length;i+=1)
			{
				message = obj[username][i];
				content = '<div class="message message-left">\
						<div class="message-text-container">\
							'+message+'\
						</div>\
						</div>';
				element = document.getElementsByClassName('message-wrapper')[0];
				element.innerHTML = element.innerHTML + content;
			}
			$.get(window.location.href);
			var divx = document.getElementById("message-container-box");
			divx.scrollTop = divx.scrollHeight;
		}
		for (var mentor in obj) {
  			var id = mentor;
  			if(obj[mentor].length != 0){
  				document.getElementById(id).innerHTML = obj[mentor].length;
  				document.getElementById(id).classList.add("unread_messages");
  			}
  			else{
  				document.getElementById(id).innerHTML = "";
  				document.getElementById(id).classList.remove("unread_messages");
  			}
  		}
		setTimeout(worker, timeout);
	  });
	})();
});