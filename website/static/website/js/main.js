$(document).ready(function() {

      // fix menu when passed
  $(document).scroll(function(){
    if($(document).scrollTop() > 70){
      $('.lapa-nav').addClass('fixed');
    }
    else
      $('.lapa-nav').removeClass('fixed'); 
  })
  $('.ui.dropdown.lapa').dropdown({
     on: 'hover',
    action: 'select'
   });

  $('.main-carousel').flickity({
    // options
    autoPlay: 3000,
    wrapAround :  true,
    contain: true,
    selectedAttraction: 0.01,
    pageDots: false
  });
  $('.news-carousel').flickity({
    groupCells : true,
    autoPlay: 3000,
    wrapAround :  true,
    contain: true,
    selectedAttraction: 0.01,
    friction:0.2
  })
});
