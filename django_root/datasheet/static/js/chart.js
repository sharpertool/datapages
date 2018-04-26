(function(w, d, target) {
    const elem = d.querySelector(target);

    const props = JSON.parse(elem.dataset.props);
    // Expected values:
    //      title,
    //      y_axis -- contains the data item name for the y_axis
    //      x_axis -- contains the data item name for the x_axis
    //
    const chart_data = JSON.parse(elem.dataset.values);

    // Remove elements to clean up DOM
    delete elem.dataset.props;
    delete elem.dataset.values;

    var chart = AmCharts.makeChart(elem, {
        "type": "serial",
        "theme": "light",
        "marginRight": 0,
        "marginLeft": 80,
        "autoMarginOffset": 20,
        "mouseWheelZoomEnabled":true,
        "dataDateFormat": "YYYY-MM-DD",
        "valueAxes": [{
            "id": "v1",
            "axisAlpha": 0,
            "position": "left",
            "ignoreAxisWidth":true
        }],
        "balloon": {
            "borderThickness": 1,
            "shadowAlpha": 0
        },
        "graphs": [{
            "id": "g1",
            "balloon":{
              "drop":true,
              "adjustBorderColor":false,
              "color":"#ffffff"
            },
            "bullet": "round",
            "bulletBorderAlpha": 1,
            "bulletColor": "#FFFFFF",
            "bulletSize": 5,
            "hideBulletsCount": 50,
            "lineThickness": 2,
            "title": props.title,
            "useLineColorForBulletBorder": true,
            "type": "smoothedLine",
            "valueField": props.y_axis,
            "balloonText": "<span style='font-size:18px;'>[[value]]</span>"
        }],
        "chartCursor": {
            "pan": true,
            "valueLineEnabled": true,
            "valueLineBalloonEnabled": true,
            "cursorAlpha":1,
            "cursorColor":"#258cbb",
            "limitToGraph":"g1",
            "valueLineAlpha":0.2,
            "valueZoomable":true
        },
        "categoryField": props.x_axis,
        "categoryAxis": {
            "parseDates": true,
            "dashLength": 1,
            "minorGridEnabled": true
        },
        "export": {
            "enabled": true
        },
        "dataProvider": chart_data
    });
})(window, document, '.data-pages-chart')

//@todo data formatter
/*
var DataShaper = function(chart_object) {
    const { headings,  data } = chart_object
    return data.map((values) => {
        return values.map((value, i) => {
            const a = {}
            a[headings[i]] = values[i]
            return a
        })
    })
}
*/
