$(document).ready(function(){
  $('#id_tags').keyup(function(){
    var tags = $(this).val();
    $.ajax({
      type: "POST",
      url: "/connect/ajax_tag_search/",
      data: {
        'tags' : tags
      },
      success: function(data){
        if(data.done == true)
        {
          var searchResult = data;
          var searchResultsLength = searchResult.data.length;
          $(".search-list")[0].innerHTML = "";
          str = "";
          for(var i = 0; i < searchResultsLength; i++)
          {
            str+= "<li><h5 class='search-name'>"+ searchResult.data[i].name +"</h5><h6 class='search-subheading'>" + searchResult.data[i].branch + ", Batch of "+ searchResult.data[i].batch +"</h6><h6 class='search-tags'>Tags : ";
            tags = searchResult.data[i].tags.join(", ")
            str+=  tags;
            str+= "</h6><a href='/connect/student_chat/"+searchResult.data[i].username+"/'>Send Connect Request</a></li>";
          }
          $(".search-list")[0].innerHTML = str;
        }
      },
      failure: function(data){
        console.log("request fail!");
      },
    });
  });
});
