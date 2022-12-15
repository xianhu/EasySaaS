/**
 * dash clientside callbacks
 * @type {any}
 */
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        render_chart: function (data) {
            let chart = echarts.init(document.getElementById(data['id_chart_div']));

            // option data
            const option = {
                xAxis: {
                    data: data['x_data'],
                },
                yAxis: {},
                series: [{
                    type: 'bar',
                    data: data['y_data'],
                }]
            };

            // set option
            chart.setOption(option);

            // event listener
            chart.on('click', function (params) {
                sessionStorage.setItem(data['id_chart_click'], JSON.stringify({
                    name: params.name,
                    value: params.value,
                    _date: new Date().getTime(),
                }));
            });
        },
    },
});