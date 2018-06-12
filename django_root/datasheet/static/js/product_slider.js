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

        update_min_height(targetPane);
    });

    var tab = productinfo.find('.panes > .pane').filter(function () {
       return !$(this).hasClass('d-none');
    });

    console.log(tab)

    update_min_height(tab);

    function get_other_targets (targetPane) {
        var targets = navLinks.map(function () {
           return $(this).data('target');
        }).toArray();

        var st = new Set(targets);
        st.delete(targetPane);
        return Array.from(st.values());
    }

    function update_min_height (targetPane) {
        var me = $(targetPane);
        var parent = me.parent();
        var height = parent.data('height');
        height = Math.max(me.height(), height);

        var csstag = $(`<style type="text/css" id="setheight">
            #product_info .panes > .pane { --attr_height: ${height}px; }
        </style>`);

        parent.data('height', height);

        if ($("#setheight").length) {
            $("#setheight").remove();
        }

        $('body').append(csstag);
    }

})();
