class Chart {
    constructor(target, props, series) {
        this.target = target
        this.series = series
        for(var i in props) {
            this[i] = props[i]
        }
    }

    render() {
        const {
            subtitle,
            legend,
            title,
            xAxis,
            yAxis,
            series,
            type,
            target
        } = this

        const formatted_series = Array.isArray(series) ? [...series] : [series]

        const options = {
            chart: {
                type,
                renderTo: target,
                plotShadow: false,
            },
            title: {
                text: subtitle
            },
            subtitle: {
                text: legend
            },
            xAxis,
            yAxis,
            legend: {
                enabled: false
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br/>',
                pointFormat: '{point.x} {point.y}'
            },
            plotOptions: {
                spline: {
                    marker: {
                        enable: false
                    }
                }
            },
            series: formatted_series
        }

        return new Highcharts.Chart(options)
    }
}


//Initialize charts
(function(w, d, target) {
    const elems = d.querySelectorAll(target);

    elems.forEach((elem, key) => {
        if(elem.dataset.props && elem.dataset.values) {
            const basic_config = JSON.parse(elem.dataset.props)

            const x_axis_config = JSON.parse(elem.dataset.x_axis_config)
            const y_axis_config = JSON.parse(elem.dataset.y_axis_config)

            const props = {
                ...basic_config,
                xAxis:  {...x_axis_config},
                yAxis: {...y_axis_config}
            }

            // Expected values:
            //      title,
            //      y_axis -- contains the data item name for the y_axis
            //      x_axis -- contains the data item name for the x_axis
            //
            const chart_data = JSON.parse(elem.dataset.values)
            // Remove elements to clean up DOM
            delete elem.dataset.props
            delete elem.dataset.values
            delete elem.dataset.x_axis_config
            delete elem.dataset.y_axis_config

            const chart = new Chart(elem, props, chart_data)

            chart.render()
        } else {
            console.error('No dataset')
        }
    });

    // Add/remote hovered class so we can adjust the
    // style of the chart when mouse is hovered
    $('.chart-container').each(function(i) {
        //
        $(this).mouseenter(function() {
            $(this).addClass('hovered')
        }).mouseleave(function() {
            $(this).removeClass('hovered')
                .removeClass('zoom')
        })
    })

    // When the zoom icon is clicked, add the 'zoom' class to the
    // card identified by the id. ID is set in the template so it
    // will be unique.
    $('.chart-card-zoom').each(function(i) {
        $(this).click(function() {
            var id = $(this).data('cardid');
            $(id).toggleClass('zoom')
        })
    })

})(window, document, '.data-pages-chart')
