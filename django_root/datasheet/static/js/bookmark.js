(function($) {
    //jump-to-section
    $("a[data-action='anchor']").click(function(e) {
        var target = $(this.getAttribute('href'));
        $('html, body').animate({
            scrollTop: $(target).offset().top - 100
        }, 1000);
        $(this).parents('li').addClass('active').siblings('li').removeClass('active');
        $('.jump-section-wrapper').trigger('click');
        e.preventDefault();
    });

    //jump-to-section-dropdown
    $('.sidebar').on('click', '.jump-section-wrapper', function(e) {
        e.preventDefault();
        var $this = $(this);
        if ($this.parents('.sidebar').find('ul').is(':not(":animated")')) {
            $this.toggleClass('open');
            $this.parents('.sidebar').find('ul').slideToggle('500');
        } else {
            console.log('already animating');
        }
    });

    $(window).on('load resize', function() {
        var headerHeight = $('#header').height();
        $('main').css('margin-top', headerHeight);
    });
})($);