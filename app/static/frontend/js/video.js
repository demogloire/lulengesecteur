(function ($) {
    //   magnific popup video
    $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-zoom-in',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: true
    });


})(jQuery);