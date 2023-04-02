/**
 * dash clientside callbacks
 * @type {any}
 */
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        render_chart: function (params) {
            console.log('render chart: ' + String(params));

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

        render_flow: function (params) {
            console.log('render flow: ' + String(params));

            // get data from params
            let id_div = params['id_div'];
            let id_button = params['id_button'];
            let id_storage = params['id_storage'];

            // add input to div
            let id_input = 'id-input-file';
            let div = document.getElementById(id_div);
            div.innerHTML = "<input id='id-input-file' type='file' name='file'/>";

            // bind button click event to input click
            document.getElementById(id_button).addEventListener('click', function (event) {
                document.getElementById(id_input).click();
            });

            // bind input change event to flow upload
            document.getElementById(id_input).addEventListener('change', function (event) {
                flow.addFile(event.target.files[0]);
                flow.upload();
            });
        },
    },
});