$(function() {
  // aos animation initialisation
  AOS.init({
    duration: 2000,
    once: true
  });

  // scroll header script here
  window.onscroll = function() {
    scrollHeader();
  };
  // Get the header
  var header = $(".navbar-bottom");
  var body = $("body");
  function scrollHeader() {
    // adding sticky class
    if (window.pageYOffset > 130) {
      $(header).addClass("sticky");
    } else {
      // removing sticky class
      $(header).removeClass("sticky");
    }
  }

  // navbar toggler script
  $(".navbar-toggler").on("click", function() {
    $(".collapse").toggleClass("show");
    $("body").toggleClass("layer-open");
    // $(header).toggleClass("sticky-not");
    $(".navbar-close").show();
  });
  $(".navbar-close").on("click", function() {
    $(".collapse").toggleClass("show");
    $(".navbar-close").hide();
    $("body").toggleClass("layer-open");
    // $(header).toggleClass("sticky-not");
    $(".dark-overlay").click(function() {
      $(".collapse").removeClass("show");
      $("body").removeClass("layer-open");
    });
  });

  // $(".navbar-bottom  .navbar-nav a").on("click", function() {
  //   $(".navbar-bottom  .navbar-nav")
  //     .find("li.active")
  //     .removeClass("active");
  //   $(this)
  //     .parent("li")
  //     .addClass("active");
  // });

});
