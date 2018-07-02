(function($, openClass) {

    var jump_items = $('.jump-menu li')
    var toggle = $('.jump-toggle')
    
    var calc_offset = function calc_offset() {
        // Return full height, with padding
        var nav_h = parseInt($('.navbar').css('height'))
        
        var mm = $('.menu-mobile')
        var h1 = mm.is(':hidden') ?
            0 : parseInt($('.menu-mobile').css('height'))
            
        var offset = nav_h + h1

        return offset
    }

    $("a[data-action='anchor']").on('click', function(e) {
        e.preventDefault()
        var self = $(this)
        var target = self.attr('href')

        var offset = calc_offset()
        
        if (target == '#bookmark_introduction') {
            $('html, body').animate({scrollTop: 0}, 1000)
        } else {
            $('html, body').animate({
                scrollTop: $(target).offset().top - offset
            }, 1000)
        }
        toggle.trigger('click')
    })

    //jump-to-section-dropdown
    $('.menu-mobile').on('click', '.jump-toggle', function(e) {
        e.preventDefault();
        console.log('Toggling menu open/closed')
        var self = $(this)
        var mnu = $('.jump-menu', self.parent())

        self.toggleClass(openClass)
        mnu.toggleClass(openClass, self.hasClass(openClass))
    });
    
    function setup_scrollspy() {
        var mm = $('.menu-mobile')
        var target = mm.is(':hidden') ?
            '#sidebar_jump_list' : '#mobile_jump_list'

        // Add a couple of pixels to scroll spy from the scrollTop value
        var offset = calc_offset() + 2

        // Update Active links when body scrolled
        $('body').scrollspy({
            target: target,
            offset: offset
        })
        console.log(`Setup scrollspy on ${target}`)
    }
    
    // setup the scrollspy on the main or mobile menu
    // If the window is re-sized, then reset it
    setup_scrollspy()
    $(window).resize(function() {
        setup_scrollspy()
    })

})(jQuery, 'open')
