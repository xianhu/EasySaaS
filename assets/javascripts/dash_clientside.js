/**
 * dash clientside callbacks
 * @type {any}
 */
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        render_chart: function (data) {
            // create a new chart
            let chart = echarts.init(document.getElementById(data['id_div']));

            // define option
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
                sessionStorage.setItem(data['id_storage'], JSON.stringify({
                    name: params.name,
                    value: params.value,
                    _timestamp: new Date().getTime(),
                }));
            });
        },

        render_flow: function (data) {
            console.log('render flow: ' + String(data));
            // add input to div
            let div = document.getElementById(data['id_div']);
            div.innerHTML = "<input id='id-input-file' type='file' name='file'/>";

            // bind button click event to input click
            document.getElementById(data['id_button']).addEventListener('click', function () {
                document.getElementById('id-input-file').click();
            });

            // bind input change event to flow upload
            document.getElementById('id-input-file').addEventListener('change', function (event) {
                flow.addFile(event.target.files[0]);
                flow.upload();
            });
        },
    },
});