(function(d, target, $) {

    const sidebar = d.querySelector(target)


    $("a[data-action='anchor']").click(function(e) {
        var target = $(this.getAttribute('href'));
        $('html, body').animate({
            scrollTop: $(target).offset().top - 135
        }, 1000);
        $(this).parents('li').addClass('active').siblings('li').removeClass('active');
        $('.jump-section-wrapper').trigger('click');
        e.preventDefault();
    })

    const floatSideBar = (e) => {
        const yCoordinate = window.pageYOffset
        const yOffset = sidebar.offsetTop - 120

        if(yOffset <= yCoordinate) {
            sidebar.classList.add('scrolled')
            return
        }

        sidebar.classList.remove('scrolled')

        return

    }

    const scrollObserver = () => {
        floatSideBar()
    }

    document.addEventListener('scroll', scrollObserver)

})(document, '.sidebar', jQuery);
