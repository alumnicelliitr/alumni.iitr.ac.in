
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

	$('#mentor_search').submit(function(e){
			e.preventDefault();
			$.ajax({
				url: "/samp/cor_api/",
				method:"POST",
				type: "json",
				dataType: "json",
				data: $(this).serialize(),
				success: function(result){
					console.log(result);
					console.log(result.mentor.length);
					var htmlString = "";
					for (var i = result.mentor.length - 1; i >= 0; i--) {
						var alumni = JSON.parse(result.mentor[i].alumni);
						var user = JSON.parse(result.mentor[i].user);
						console.log(alumni[i].fields.year_passout);
						console.log(user[i].fields.name);
						htmlString = htmlString.concat("<div class='col-md-4'>");
						htmlString = htmlString.concat("<span style='float: left;margin-right:4px;'><input type='checkbox' name='mentor_preference'></span>");
						htmlString = htmlString.concat("<span><div class='card text-center' id='"+ user[i].fields.username +"'>");
						htmlString = htmlString.concat("<div class='text-center mentee-card-image'>");	
						htmlString = htmlString.concat("<img class='rounded-circle mentee-user-profile' src='/media/"+ user[i].fields.photo +"'>");
						htmlString = htmlString.concat("</div>");
						htmlString = htmlString.concat("<div class='card-block'>");
						htmlString = htmlString.concat("<h4 class='card-title'>"+ user[i].fields.name +"</h4>");
						htmlString = htmlString.concat("<hr>");
						htmlString = htmlString.concat("<div class='card-text'>");
						htmlString = htmlString.concat("<p>"+ alumni[i].fields.branch +"</p>");
						htmlString = htmlString.concat("<span class='badge badge-default'></span>");
						htmlString = htmlString.concat("</div>");
						htmlString = htmlString.concat("<br>");
						htmlString = htmlString.concat("<button class='cor_request_connect btn-block btn btn-info' data-toggle='modal' data-target='#cor_success_modal' data-user='{{ mentor.user.username }}'>Connect</button>");
						htmlString = htmlString.concat("</div>");
						htmlString = htmlString.concat("</div></span>");
						console.log(htmlString);
						$('#search-results-container').html(htmlString);
					}
					
					// for (var i = mentors.length - 1; i >= 0; i--) {
					// 	console.log(users[i].fields.name);
					// 	htmlString = htmlString.concat("<div class='col-md-4'>");
					// 	htmlString = htmlString.concat("<div class='card text-center'>");
					// 	htmlString = htmlString.concat("<div class='text-center mentee-card-image'>");	
					// 	htmlString = htmlString.concat("<img class='rounded-circle mentee-user-profile' src='/media/{{ mentor.user.photo }}'>");
					// 	htmlString = htmlString.concat("</div>");
					// 	htmlString = htmlString.concat("<div class='card-block'>");
					// 	htmlString = htmlString.concat("<h4 class='card-title'>"+ users[i].fields.name +"</h4>");
					// 	htmlString = htmlString.concat("<hr>");
					// 	htmlString = htmlString.concat("<div class='card-text'>");
					// 	htmlString = htmlString.concat("<p>"+ mentors[0].fields.branch +"</p>");
					// 	htmlString = htmlString.concat("<span class='badge badge-default'></span>");
					// 	htmlString = htmlString.concat("</div>");
					// 	htmlString = htmlString.concat("<br>");
					// 	htmlString = htmlString.concat("<button class='cor_request_connect btn-block btn btn-info' data-toggle='modal' data-target='#cor_success_modal' data-user='{{ mentor.user.username }}'>Connect</button>");
					// 	htmlString = htmlString.concat("</div>");
					// 	htmlString = htmlString.concat("</div>");
					// 	console.log(htmlString);
					// 	$('#search-results-container').html(htmlString);
					// }
				},
			});
			
		});
	});