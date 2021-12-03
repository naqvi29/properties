/*----------------------
   Template Name: Haven Real Estate html5 template
    Description: This is html5 template
    Author: Devitems
    Version: 1.0
---------------------------*/
(function ($) {
  "use strict";



  /*-------------------------------------------
   	 jQuery MeanMenu
   --------------------------------------------- */
  jQuery('nav#dropdown').meanmenu();

  /*-------------------------------------------
  	 wow js active
  --------------------------------------------- */
  new WOW().init();

  /*-------------------------------------------
  	 toltip js active
  --------------------------------------------- */
  $('[data-toggle="tooltip"]').tooltip();

  /*----------------------------
     stickey menu
  ----------------------------*/
  $(window).on('scroll', function () {
    var scroll = $(window).scrollTop();
    if (scroll < 265) {
      $(".sticky-header").removeClass("sticky");
    } else {
      $(".sticky-header").addClass("sticky");
    }
  });

  $('.close-home').on('click', function () {
    $('.find-home-box').addClass('fadeOut');

  });

  /*----------------------
		Nivo slider activation
	----------------------*/
  $('#mainSlider').nivoSlider({
    directionNav: true,
    controlNavThumbs: false,
    animSpeed: 1000,
    slices: 10,
    pauseTime: 5000,
    pauseOnHover: true,
    controlNav: false,
    manualAdvance: true,
    prevText: '<i class="fa fa-angle-left"></i>',
    nextText: '<i class="fa fa-angle-right"></i>'
  });

  
  /*-------------------------
    Owl Carousel Slider
  ------------------------------ */
  var homeSlider = $(".js-slider-active");

  homeSlider.owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    items: 1,
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
  });

  homeSlider.on('translate.owl.carousel', function(){
		var animation = $('[data-animation]');
		animation.each(function(){
			var anim_name = $(this).data('animation');
			$(this).removeClass('animated ' + anim_name).css('opacity', '0');
		});
	});

	$('[data-delay]').each(function(){
		var anim_del = $(this).data('delay');
		$(this).css('animation-delay', anim_del);
	});


	$('[data-duration]').each(function(){
		var anim_dur = $(this).data('duration');
		$(this).css('animation-duration', anim_dur);
	});

	homeSlider.on('translated.owl.carousel', function(){
		var layer = homeSlider.find('.owl-item.active').find('[data-animation]');
		layer.each(function(){
			var anim_name = $(this).data('animation');
			$(this).addClass('animated ' + anim_name).css('opacity', '1');
		});
	});
  /*-------------------------
    slider active
  ------------------------------ */
  $(".property-list").owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    margin: 30,
    items: 3,
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    responsive: {
      0: {
        items: 1,
      },
      767: {
        items: 2
      },
      1199: {
        items: 3
      }
    }
  });
  
  $(".lataest-property-carousel").owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    margin: 30,
    items: 4,
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    responsive: {
      0: {
        items: 1,
      },
      767: {
        items: 3
      },
      991: {
        items: 4
      }
    }
  });
  
  $(".lataest-property-carousel-2").owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    margin: 30,
    items: 3,
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    responsive: {
      0: {
        items: 1,
      },
      767: {
        items: 2
      },
      991: {
        items: 3
      }
    }
  });


  $(".single-property-tab-slider").owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    dots: false,
    nav: true,
    items: 6,
    margin: 20,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    responsive: {
      0: {
        items: 1,
      },
      320: {
        items: 2,
      },
      479: {
        items: 3,
      },
      767: {
        items: 5
      },
      991: {
        items: 5
      },
      1199: {
        items: 6
      }
    }
  });

  $(".happy-client-list").owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    margin: 30,
    dots: false,
    nav: true,
    items: 4,
    responsive: {
      0: {
        items: 1,
      },
      767: {
        items: 1
      },
      991: {
        items: 3
      },
      1199: {
        items: 4
      }
    }
  });

  $(".testimonial-carousel").owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    margin: 30,
    dots: false,
    nav: true,
    navText: ["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
    items: 2,
    responsive: {
      0: {
        items: 1,
      },
      991: {
        items: 2
      }
    }
  });

  $(".brand-list").owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    dots: false,
    nav: false,
    items: 5,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
    itemsDesktop: [1199, 4],
    itemsDesktopSmall: [991, 3],
    itemsTablet: [768, 2],
    itemsMobile: [479, 1],
    responsive: {
      0: {
        items: 1,
      },
      479: {
        items: 2,
      },
      767: {
        items: 3
      },
      991: {
        items: 4
      },
      1199: {
        items: 5
      }
    }
  });
  $(".property_list").owlCarousel({
    autoplay: false,
    smartSpeed: 2000,
    dots: false,
    nav: true,
    items: 1,
    navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
  });

  /*------------------------------------    
    Search Bar
  --------------------------------------*/

  $('.search-icon a').on('click', function () {
    $('.header').toggleClass('search-box-show');
    return false;
  });

  $('.search-close-btn a').on('click', function () {
    $('.header').toggleClass('search-box-show');
    return false;
  });
  /*----------------------    
      magnificPopup active
  --------------*/
  $('.play-button a').magnificPopup({
    disableOn: 0,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 160,
    preloader: true,

    fixedContentPos: false
  });
  /*----------------------    
      collpase active
  --------------*/
  $(".accordion-active").collapse({
    accordion: true,
    open: function () {
      this.slideDown(550);
    },
    close: function () {
      this.slideUp(550);
    }
  });


  /*--------------------
      You tube video active
  -------------------------*/
  $(".youtube-bg").YTPlayer({
    videoURL: "https://youtu.be/vb5KLYAtPIs",
    containment: '.youtube-bg',
    mute: true,
    loop: true,
    showControls: true

  });

  /*--------------------------
		 Parallax active
	----------------------*/
  $('.parallax').parallax("50%", 0.5);

  /*------------------
      5. Price Slider
  --------------------------*/
  $("#slider-range").slider({
    range: true,
    min: 20,
    max: 2500,
    values: [600, 2000],
    slide: function (event, ui) {
      $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
    }
  });
  $("#amount").val("$" + $("#slider-range").slider("values", 0) +
    " - $" + $("#slider-range").slider("values", 1));


  /*--------------------------
    Counter Up
  ---------------------------- */
  $('.counter').counterUp({
    delay: 70,
    time: 5000
  });

  /*-------------------------------------------
    	scrollUp jquery active
    --------------------------------------------- */
  $.scrollUp({
    scrollText: '<i class="icofont icofont-simple-up"></i>',
    easingType: 'linear',
    scrollSpeed: 900,
    animation: 'fade'
  });

  /*-----------------------------
  Loader activation here. 
  -------------------------------*/
  $("#fakeLoader").fakeLoader({
    timeToHide: 1500,
    zIndex: 999999,
    spinner: "spinner1", //Options: 'spinner1', 'spinner2', 'spinner3', 'spinner4', 'spinner5', 'spinner6', 'spinner7' 
    bgColor: "#fff"
  });


})
(jQuery);