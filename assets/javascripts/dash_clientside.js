/**
 * dash clientside callbacks
 * @type {any}
 */
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        render_chart: function (data, id_chart, id_store) {
            let chart = echarts.init(document.getElementById(id_chart));

            // demo data
            const option = {
                xAxis: {
                    data: data['x_data'],
                },
                yAxis: {},
                series: [
                    {
                        type: 'bar',
                        data: data['y_data'],
                    }
                ]
            };

            // set option
            chart.setOption(option);

            // event listener
            chart.on('click', function (params) {
                sessionStorage.setItem(id_store, JSON.stringify(params));
            });
        },
    },
});