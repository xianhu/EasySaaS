/**
 * dash clientside callbacks
 * @type {any}
 */
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        render_chart: function (data) {
            console.log(data)
            let id_chart = data['id_chart'];
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
            let id_click = data['id_click'];
            chart.on('click', function (params) {
                sessionStorage.setItem(id_click, JSON.stringify({
                    name: params.name,
                    value: params.value
                }));
            });
        },
    },
});