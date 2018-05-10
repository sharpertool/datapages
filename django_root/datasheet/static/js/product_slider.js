(function () {
    var productinfo = $('.product-slider #product_info');
    var panes = productinfo.find('.tab-content > .tab-pane');
    var maxHeight = getPanesMaxHeight(panes);

    $.each(panes, function () {
       if ($(this).height() < maxHeight) {
           $(this).height(maxHeight);
       }
    });


    function getPanesMaxHeight(panes) {
        var heights = [];

        $.each(panes, function () {
            heights.push($(this).height())
        });

        return Math.max(...heights);
    }
})();