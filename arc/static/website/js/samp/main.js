$(document).ready(function() {
	if (document.getElementsByClassName("mentor_error_message").innerHTML != undefined ) {
		$('#LoginModal').modal('show');
	}

	function assignFormClass(){
		document.getElementById("id_content").className += "form-control";
	}

	$(".cor_request_connect").click(function(){
		var btn = $(this);
		var user = btn.attr('data-user');
		if (!btn.hasClass('disabled')) {
			$.ajax({
				url: "/samp/cor_request/" + user,
				type: "GET",
				success: function(result){
					if(result === 'success') {
						$('#modal_message').html("Mentor has been requested! You will be able to message him once he connects with you.");
						btn.addClass('disabled');
					}
				}
			});
		}
	})
});
