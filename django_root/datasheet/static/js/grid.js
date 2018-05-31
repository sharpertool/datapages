(function($, agGrid) {
    var containers = $("[data-display=grid]");

    $.each(containers, function(index, value) {
         var data = $(this).data('json');
         console.log(data);

        new agGrid.Grid(this, {
            columnDefs: data.heading,
            rowData: data.rows,
            autoGroupColumnDef: data.groupColumnDef ? data.groupColumnDef : {},
            groupDefaultExpanded: -1
        });
    })
})($, agGrid)