$("tr").not(':first').hover(
    function () {
      $(this).css("background","#FFFFFF");
      $(this).find("td").css("color","#171A1F");
    }, 
    function () {
      $(this).css("background","");
      $(this).find("td").css("color","");
    }
  );

  $(".content-table th.table--add--button").hover(
    function () {
        $(this).css("background","#FFFFFF"); 
        $(this).css("color","#171A1F"); 
    }, 
    function () {
        $(this).css("background","");
        $(this).css("color",""); 
    }
);

jQuery(document).ready(function($) { 
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
    $(".table--add--button").click(function() {
      window.location = $(this).data("href");
  });
});