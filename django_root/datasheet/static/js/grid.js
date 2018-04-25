(function($, agGrid) {
    var containers = $("[data-display=grid]");

    $.each(containers, function(index, value) {
         var data = $(this).data('json');

        new agGrid.Grid(this, {
            columnDefs: data.heading,
            rowData: data.rows
        });
    })
})($, agGrid)