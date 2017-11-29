
$(document).ready(function() {
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');
	$.ajaxSetup({
        headers: {
           "X-CSRFToken": getCookie("csrftoken")
        }
    });

	$('#cor_search').submit(function(e){
			e.preventDefault();
			$.ajax({
				url: "/samp/cor/",
				method:"POST",
				type: "json",
				dataType: "json",
				data: $(this).serialize(),
				success: function(result){
					console.log(result);
					var mentors = JSON.parse(result.mentors);
					var users = JSON.parse(result.users);
					console.log(mentors);
					var htmlString = "";
					for (var i = mentors.length - 1; i >= 0; i--) {
						console.log(users[i].fields.name);
						htmlString = htmlString.concat("<div class='col-md-4'>");
						htmlString = htmlString.concat("	<div class='card text-center'>");
						htmlString = htmlString.concat("		<div class='text-center mentee-card-image'>");	
						htmlString = htmlString.concat("			<img class='rounded-circle mentee-user-profile' src='/media/"+ users[i].fields.photo +"'>");
						htmlString = htmlString.concat("		</div>");
						htmlString = htmlString.concat("		<div class='card-block'>");
						htmlString = htmlString.concat("			<h4 class='card-title'>"+ users[i].fields.name +"</h4>");
						htmlString = htmlString.concat("			<hr>");
						htmlString = htmlString.concat("			<div class='card-text'>");
						htmlString = htmlString.concat("				<p>"+ mentors[i].fields.branch +"</p>");
						htmlString = htmlString.concat("				<a href='"+ mentors[i].fields.linked_in +"' target='_blank'><i class='fa fa-linkedin-square' aria-hidden='true'></i></a>");
						htmlString = htmlString.concat("				<a href='"+ mentors[i].fields.facebook +"' target='_blank' class='m-l-10'><i class='fa fa-facebook-official' aria-hidden='true'></i></a>");
						htmlString = htmlString.concat("				<a href='"+ mentors[i].fields.website +"' target='_blank' class='m-l-10'><i class='fa fa-globe' aria-hidden='true'></i></a>");
						htmlString = htmlString.concat("				<a href='mailto:"+ mentors[i].fields.email +"' target='_top' class='m-l-10'><i class='fa fa-envelope' aria-hidden='true'></i></a>");
						htmlString = htmlString.concat("			</div>");
						htmlString = htmlString.concat("			<br>");
						htmlString = htmlString.concat("			<button class='cor_request_connect btn-block btn btn-info' data-toggle='modal' data-target='#cor_success_modal' data-user='{{ mentor.user.username }}'>Connect</button>");
						htmlString = htmlString.concat("		</div>");
						htmlString = htmlString.concat("	</div>");
						htmlString = htmlString.concat("</div>");
						$('#search-results-container').html(htmlString);
					}
				},
			});
			
		});
	});