(function($) {
var App = { init: function() { App.HomepageHeight();
                               App.HomepageOpacity();          // changes homepage opacity on scroll
							   App.MaxImage_Video();           // homepage background - video
							   App.MaxImage_Slider();          // homepage background - image slider
							   App.MaxImage_Single();          // homepage background - vingle image
							   App.ScrollToSomeplace();        // script resposible for smooth scrolling after clicking on menu item
							   App.ContactForm();              // contact form
							   App.Fit_Vids();                 // responsive videos
							   App.Reviews();                  // reviews carousel
							   App.Screenshots_Carousel();     // screenshots carousel 
							   App.Nivo_Lightbox();            // lightbox
							   App.Elements_animation();       // animations
							   },

	// Homepage Height
	HomepageHeight: function() {
	"use strict"; 
	    var h = window.innerWidth/4;
	    $('.hero_fullscreen.background_solid').css('padding-bottom', h );
	    
	},
	
	
	// Homepage Opacity - for single background image version
	HomepageOpacity: function() {
    "use strict"; 
        var h = window.innerHeight;
        $(window).on('scroll', function() {
            var st = $(this).scrollTop();
            $('#maximage_single').css('opacity', (1-st/h) );
        });
    },
	
	
	// MaxImage Fullscreen Background Slider
	MaxImage_Video: function() {
	"use strict";
	    jQuery('video, object').maximage('maxcover');
	    
	    // detecting if browser is mobile and disabling the video background, leaving only poster as bg.
		if( navigator.userAgent.match(/Android/i)
		|| navigator.userAgent.match(/webOS/i)
		|| navigator.userAgent.match(/iPhone/i)
		|| navigator.userAgent.match(/iPad/i)
		|| navigator.userAgent.match(/iPod/i)
		|| navigator.userAgent.match(/BlackBerry/i)
		|| navigator.userAgent.match(/Windows Phone/i)
		 ){
		    $('#maximage_video video').css('display', 'none' );
		    classie.add( document.getElementById( 'maximage_video' ), 'mobile_novideo' );
		  };
	},
	
	
	// MaxImage Fullscreen Background Slider
	MaxImage_Slider: function() {
	"use strict"; 
	    $('#maximage_slider').maximage();
	},
	
	
	// MaxImage Fullscreen Background Slider
	MaxImage_Single: function() {
	"use strict";
	    $('#maximage_single').maximage();
	},
	
	
	// Scroll To ...
    ScrollToSomeplace: function() {
    $('.go_to_home').click(function () {$.scrollTo('.hero_fullscreen',1000,{easing:'easeInOutExpo','axis':'y'});return false}); 
    
    var lastId,
    navbarheight = $("#menu_bar").outerHeight()+1;
    topMenu = $('.menu_bar_navigation, .navigation_desktop, #mobile_menu_content, .cta_button_area');
    menuItems = topMenu.find('a');
    scrollItems = menuItems.map(function(){
        var item = $($(this).attr("href"));
        if (item.length) { return item; }
    });
 
    menuItems.click(function(e){
        var href = $(this).attr("href"),
        offsetTop = href === "#" ? 0 : $(href).offset().top-navbarheight+2;
        $('html, body').stop().animate({ scrollTop: offsetTop  }, 1000, 'easeInOutExpo');
        e.preventDefault();
    });
 
    $(window).scroll(function(){
        // Get container scroll position
        var fromTop = $(this).scrollTop()+navbarheight;

        // Get id of current scroll item
        var cur = scrollItems.map(function(){
                                if ($(this).offset().top < fromTop)
                                return this;
                                });
        // Get the id of the current element
        cur = cur[cur.length-1];
        var id = cur && cur.length ? cur[0].id : "";

        if (lastId !== id) {
        lastId = id;
        // Set/remove active class
        menuItems
        .parent().removeClass("active")
        .end().filter("[href=#"+id+"]").parent().addClass("active");
        }                   
    });
    
    },
        
    
    // Contact Form
    ContactForm: function() {
	     "use strict";
	    var options = {target: "#alert"}
	    $("#contact-form").ajaxForm(options);
    },
    
    
    // Elements Animation
    Elements_animation: function() {
		$('#more_info').waypoint(function() {
            setTimeout(function(){$('.more_info_anim1').addClass('animated fadeInUp')},0);
        }, { offset: '50%' });    
    
    	$('#feature1').waypoint(function() {
            setTimeout(function(){$('.more_info_anim2').addClass('animated fadeInLeft')},0);
            setTimeout(function(){$('.more_info_anim3').addClass('animated fadeInRight')},0);
        }, { offset: '50%' }); 
		
        $('#feature2').waypoint(function() {
            setTimeout(function(){$('.more_info_anim4').addClass('animated fadeInLeft')},0);
            setTimeout(function(){$('.more_info_anim5').addClass('animated fadeInRight')},0);
        }, { offset: '50%' }); 
    
		$('#feature3').waypoint(function() {
            setTimeout(function(){$('.more_info_anim6').addClass('animated fadeInUp')},0);
            setTimeout(function(){$('.more_info_anim7').addClass('animated fadeInLeft')},200);
            setTimeout(function(){$('.more_info_anim8').addClass('animated fadeInLeft')},400);
            setTimeout(function(){$('.more_info_anim9').addClass('animated fadeInRight')},200);
            setTimeout(function(){$('.more_info_anim10').addClass('animated fadeInRight')},400);
        }, { offset: '50%' }); 
    
    
    
    	$('#about_video').waypoint(function() {
            setTimeout(function(){$('.about_video_anim1').addClass('animated fadeInUp')},0);
            setTimeout(function(){$('.about_video_anim2').addClass('animated fadeInUp')},200);
            setTimeout(function(){$('.about_video_anim3').addClass('animated fadeInUp')},400);
            setTimeout(function(){$('.about_video_anim4').addClass('animated fadeInUp')},600);
            setTimeout(function(){$('.about_video_anim5').addClass('animated fadeInUp')},800);
            setTimeout(function(){$('.about_video_anim6').addClass('animated fadeInUp')},1000);
            setTimeout(function(){$('.about_video_anim7').addClass('animated fadeInUp')},1200);
            setTimeout(function(){$('.about_video_anim8').addClass('animated fadeInUp')},1400);
            setTimeout(function(){$('.about_video_anim9').addClass('animated fadeInUp')},1600);
            setTimeout(function(){$('.about_video_anim10').addClass('animated fadeInUp')},2000);
        }, { offset: '50%' });
        
        $('#reviews').waypoint(function() {
            setTimeout(function(){$('.reviews_anim1').addClass('animated fadeInUp')},0);
            setTimeout(function(){$('.reviews_anim2').addClass('animated fadeInUp')},200);
            setTimeout(function(){$('.reviews_anim3').addClass('animated fadeInLeft')},600);
            setTimeout(function(){$('.reviews_anim4').addClass('animated fadeInLeft')},400);
            setTimeout(function(){$('.reviews_anim5').addClass('animated fadeInRight')},400);
            setTimeout(function(){$('.reviews_anim6').addClass('animated fadeInRight')},600);
            setTimeout(function(){$('.reviews_anim7').addClass('animated fadeInUp')},1200);
            setTimeout(function(){$('.reviews_anim8').addClass('animated fadeInUp')},1400);
            setTimeout(function(){$('.reviews_anim9').addClass('animated fadeInUp')},1600);
            setTimeout(function(){$('.reviews_anim10').addClass('animated fadeInUp')},1800);
        }, { offset: '50%' }); 
        
        
        
        $('#screenshots').waypoint(function() {
            setTimeout(function(){$('.screenshots_anim1').addClass('animated fadeInUp')},0);
            setTimeout(function(){$('.screenshots_anim2').addClass('animated fadeInUp')},200);
            setTimeout(function(){$('.screenshots_anim3').addClass('animated fadeInUp')},300);
            setTimeout(function(){$('.screenshots_anim4').addClass('animated fadeInUp')},400);
            setTimeout(function(){$('.screenshots_anim5').addClass('animated fadeInUp')},500);
            setTimeout(function(){$('.screenshots_anim6').addClass('animated fadeInUp')},600);
            setTimeout(function(){$('.screenshots_anim7').addClass('animated fadeInUp')},700);
            setTimeout(function(){$('.screenshots_anim8').addClass('animated fadeInUp')},800);
            setTimeout(function(){$('.screenshots_anim9').addClass('animated fadeInUp')},900);
            setTimeout(function(){$('.screenshots_anim10').addClass('animated fadeInUp')},1000);
        }, { offset: '50%' });
        
        
        $('#pricing').waypoint(function() {
            setTimeout(function(){$('.pricing_anim1').addClass('animated fadeInUp')},0);
            setTimeout(function(){$('.pricing_anim2').addClass('animated fadeInUp')},200);
            setTimeout(function(){$('.pricing_anim3').addClass('animated fadeInUp')},400);
            setTimeout(function(){$('.pricing_anim4').addClass('animated fadeInUp')},600);
            setTimeout(function(){$('.pricing_anim5').addClass('animated fadeInUp')},800);
            setTimeout(function(){$('.pricing_anim6').addClass('animated fadeInUp')},1000);
            setTimeout(function(){$('.pricing_anim7').addClass('animated fadeInUp')},1200);
            setTimeout(function(){$('.pricing_anim8').addClass('animated fadeInUp')},1400);
            setTimeout(function(){$('.pricing_anim9').addClass('animated fadeInUp')},1600);
            setTimeout(function(){$('.pricing_anim10').addClass('animated fadeInUp')},1800);
        }, { offset: '50%' });
        
        $('#team').waypoint(function() {
            setTimeout(function(){$('.team_anim1').addClass('animated fadeInUp')},0);
            setTimeout(function(){$('.team_anim2').addClass('animated fadeInLeft')},400);
            setTimeout(function(){$('.team_anim3').addClass('animated fadeInLeft')},200);
            setTimeout(function(){$('.team_anim4').addClass('animated fadeInRight')},200);
            setTimeout(function(){$('.team_anim5').addClass('animated fadeInRight')},400);
            setTimeout(function(){$('.team_anim6').addClass('animated fadeInUp')},1000);
            setTimeout(function(){$('.team_anim7').addClass('animated fadeInUp')},1200);
            setTimeout(function(){$('.team_anim8').addClass('animated fadeInUp')},1400);
            setTimeout(function(){$('.team_anim9').addClass('animated fadeInUp')},1600);
            setTimeout(function(){$('.team_anim10').addClass('animated fadeInUp')},1800);
        }, { offset: '50%' });
        
        $('#cta_download').waypoint(function() {
            setTimeout(function(){$('.cta_download_anim1').addClass('animated fadeInUp')},0);
            setTimeout(function(){$('.cta_download_anim2').addClass('animated fadeInUp')},200);
            setTimeout(function(){$('.cta_download_anim3').addClass('animated fadeInUp')},400);
            setTimeout(function(){$('.cta_download_anim4').addClass('animated fadeInUp')},600);
            setTimeout(function(){$('.cta_download_anim5').addClass('animated fadeInUp')},800);
            setTimeout(function(){$('.cta_download_anim6').addClass('animated fadeInUp')},1000);
            setTimeout(function(){$('.cta_download_anim7').addClass('animated fadeInUp')},1200);
            setTimeout(function(){$('.cta_download_anim8').addClass('animated fadeInUp')},1400);
            setTimeout(function(){$('.cta_download_anim9').addClass('animated fadeInUp')},1600);
            setTimeout(function(){$('.cta_download_anim10').addClass('animated fadeInUp')},1800);
        }, { offset: '50%' });
        
        $('#contact').waypoint(function() {
            setTimeout(function(){$('.contact_anim1').addClass('animated fadeInUp')},0);
            setTimeout(function(){$('.contact_anim2').addClass('animated fadeInUp')},200);
            setTimeout(function(){$('.contact_anim3').addClass('animated fadeInUp')},400);
            setTimeout(function(){$('.contact_anim4').addClass('animated fadeInUp')},600);
            setTimeout(function(){$('.contact_anim5').addClass('animated fadeInUp')},800);
            setTimeout(function(){$('.contact_anim6').addClass('animated fadeInUp')},1000);
            setTimeout(function(){$('.contact_anim7').addClass('animated fadeInUp')},1200);
            setTimeout(function(){$('.contact_anim8').addClass('animated fadeInUp')},1400);
            setTimeout(function(){$('.contact_anim9').addClass('animated fadeInUp')},1600);
            setTimeout(function(){$('.contact_anim10').addClass('animated fadeInUp')},1800);
        }, { offset: '50%' });
          
        
    },
    
    
    // Nivo Lightbox
    Nivo_Lightbox: function() {
	    $('.screenshot a').nivoLightbox({
		    effect: 'slideDown'    
	    });	
    },
    
    
    // Fit Vids
    Fit_Vids: function() {
	    $(".about_video_player").fitVids();	
    },
    
    
    // Reviews Carousel
    Reviews: function() {
	    $(".owl-carousel").owlCarousel({
		    loop:true,
		    singleItem : true,
	    });	
    },
    
    // Screenshots Carousel
    Screenshots_Carousel: function() {
	    $(".owl-carousel-screenshots").owlCarousel({
			loop:true,
		    items : 7,
			itemsDesktop : [1200,7], 
			itemsDesktopSmall : [900,6], 
			itemsTablet: [600,4], 
			itemsMobile : [400,2]     
	    });	
    },    

}

$(function() {
  App.init();
  $(window).resize(App.HomepageHeight);
    
});

})(jQuery);