/**
 * dash clientside callbacks
 * @type {any}
 */
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    ns_flow: {
        render_flow: function (params) {
            console.log('render flow: ' + JSON.stringify(params));

            // get data from params
            let id_div = params['id_div'];
            let id_button = params['id_button'];

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