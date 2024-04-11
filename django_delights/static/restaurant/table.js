$("tr").not(':first').hover(
    function () {
      $(this).css("background","#d9d9d9");
    }, 
    function () {
      $(this).css("background","");
    }
  );

jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});