(function () {
    var productinfo = $('.product-slider #product_info');
    var navpills = productinfo.find('.nav.nav-pills');
    var navLinks = navpills.find('.nav-link');

    navLinks.click(function (e) {
        e.preventDefault();
        e.stopPropagation();

        var targetPane = $(this).data('target');
        navpills.find('.nav-link.active').removeClass('active');
        $(this).addClass('active');

        var otherTargetPanes = get_other_targets(targetPane);

        var cActive = '';
        var cOther = 'd-none';

        otherTargetPanes.map(function (el) {
           $(el).removeClass(cActive).addClass(cOther);
        });

        $(targetPane).removeClass(cOther).addClass(cActive);

    });

    var tab = productinfo.find('.panes > .pane').filter(function () {
       return !$(this).hasClass('d-none');
    });

    function get_other_targets (targetPane) {
        var targets = navLinks.map(function () {
           return $(this).data('target');
        }).toArray();

        var st = new Set(targets);
        st.delete(targetPane);
        return Array.from(st.values());
    }

})();
