/**
 * dash clientside callbacks - ns_echarts
 * @type {any}
 */
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    ns_echarts: {
        render_chart: function (params) {
            console.log('render chart: ' + JSON.stringify(params));

            // get data from params
            let id_div = params['id_div'];
            let id_storage = params['id_storage'];

            // create a new chart
            let chart = echarts.init(document.getElementById(id_div));

            // define option
            const option = {
                xAxis: {
                    data: params['x_data'],
                },
                yAxis: {},
                series: [{
                    type: 'bar',
                    data: params['y_data'],
                }]
            };

            // set option
            chart.setOption(option);

            // event listener
            chart.on('click', function (params) {
                sessionStorage.setItem(id_storage, JSON.stringify({
                    name: params.name,
                    value: params.value,
                    _timestamp: new Date().getTime(),
                }));
            });
        },
    },
});