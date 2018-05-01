class Chart {
    constructor(target, props, series) {
        this.title = props.title
        this.xAxis = props.x_axis
        this.yAxis = props.y_axis
        this.series = series
        this.type = props.type
        this.target = target
        this.legend = props.legend
        this.subtitle = props.subtitle
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
        const options = {
            chart: {
                type,
                renderTo: target,
                plotShadow:false,
            },
            title: {
                text: subtitle
            },
            subtitle: {
                text: legend
            },
            xAxis: {
                reversed: false,
                title: {
                    enabled: true,
                    text: xAxis
                },
                labels: {
                    format: '{value}'
                },
                maxPadding: 0.05,
                showLastLabel: true
            },
            yAxis: {
                title: {
                    text: yAxis
                },
                labels: {
                    format: '{value}°'
                },
                lineWidth: 2
            },
            legend: {
                enabled: false
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br/>',
                pointFormat: '{point.x} km: {point.y}°C'
            },
            plotOptions: {
                spline: {
                    marker: {
                        enable: false
                    }
                }
            },
            series: [series]
        }

        return new Highcharts.Chart(options)
    }
}


//Initialize charts
(function(w, d, target) {
    const elems = d.querySelectorAll(target);

    elems.forEach((elem, key) => {
        if(elem.dataset.props && elem.dataset.values) {
            const props = JSON.parse(elem.dataset.props);
            // Expected values:
            //      title,
            //      y_axis -- contains the data item name for the y_axis
            //      x_axis -- contains the data item name for the x_axis
            //
            const chart_data = JSON.parse(elem.dataset.values)
            // Remove elements to clean up DOM
            delete elem.dataset.props
            delete elem.dataset.values

            const chart = new Chart(elem, props, chart_data)

            chart.render()
        } else {
            console.error('No dataset')
        }
    });

    $('.chart-container').each(function(i) {
        console.log('Register handlers on chart-container')
        $(this).mouseenter(function() {
            console.log("Mouse entered chart")
            $(this).addClass('hovered')
        }).mouseleave(function() {
            console.log("Mouse left chart")
            $(this).removeClass('hovered')
        })
    })

})(window, document, '.data-pages-chart')
