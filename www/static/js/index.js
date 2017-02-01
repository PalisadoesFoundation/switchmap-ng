$(document).ready(function () {
  var $home_button = $("#home-button");
  var $search_button = $("#search-button");
  var $search_box = $("#search-wrapper");

  $home_button.on("click", function(e){
    e.preventDefault();
    console.log("Clicked");
  });

});
