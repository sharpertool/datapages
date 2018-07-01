(function($, openClass) {
    
    var jump_items = $('.jump-menu li')
    var toggle = $('.jump-toggle')

    $("a[data-action='anchor']").on('click', function(e) {
        e.preventDefault()
        var self = $(this)
        var target = self.attr('href')
        // Return full height, with padding
        var nav_h = $('.navbar').css('height')
        var h1 = $('.sidebar-mobile').css('height')
        console.log(`Height of the mobile sidebar is ${h1}`)
        $('html, body').animate({
            scrollTop: $(target).offset().top - (114 + parseInt(h1))
        }, 1000);
        jump_items.removeClass('active')
        $(this).parent().addClass('active')
        toggle.trigger('click')
    })
    
    //jump-to-section-dropdown
    $('.sidebar-mobile').on('click', '.jump-toggle', function(e) {
        e.preventDefault();
        console.log('Toggling menu open/closed')
        var self = $(this)
        var mnu = $('.jump-menu', self.parent())

        self.toggleClass(openClass)
        mnu.toggleClass(openClass, self.hasClass(openClass))
    });

})(jQuery, 'open');
