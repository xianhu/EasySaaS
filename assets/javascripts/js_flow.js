/**
 * js_flow: include initial code and client side callbacks
 */
// initial code
const flow = new Flow({
    target: '/upload',
    testChunks: false,
    uploadMethod: 'POST',
    chunkSize: 1024 * 1024,
    simultaneousUploads: 1,
    allowDuplicateUploads: true,
    progressCallbacksInterval: 1000,
});
console.log('flow object created');

// id of storage, used to store flow events
let id_storage_flow = 'id-analysis-upload-storage-flow';

// define flow events
flow.on('fileAdded', function (file) {
    sessionStorage.setItem(id_storage_flow, JSON.stringify({
        status: 'fileAdded',
        file_name: file.name,
        file_size: file.size,
        _timestamp: new Date().getTime(),
    }));
    console.log('file added');
});

// define flow events
flow.on('fileProgress', function (file) {
    let percent = Math.floor(file.progress() * 100);
    console.log('file progress: ' + percent + '%');
});

// define flow events
flow.on('fileSuccess', function (file, message) {
    sessionStorage.setItem(id_storage_flow, JSON.stringify({
        status: 'fileSuccess',
        file_name: file.name,
        file_size: file.size,
        _timestamp: new Date().getTime(),
    }));
    console.log('file success', message);
});

// define flow events
flow.on('fileError', function (file, message) {
    sessionStorage.setItem(id_storage_flow, JSON.stringify({
        status: 'fileError',
        file_name: file.name,
        file_size: file.size,
        _timestamp: new Date().getTime(),
    }));
    console.log('file error', message);
});

// client side callbacks
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    ns_flow: {
        render_flow: function (params) {
            console.log('render flow:' + JSON.stringify(params));

            // get data from params
            let id_div = params['id_div'];
            let id_button = params['id_button'];

            // add input to div
            let id_input = 'id-input-file';
            let div = document.getElementById(id_div);
            div.innerHTML = "<input id='id-input-file' type='file' name='file' />";

            // bind button click event to input click
            document.getElementById(id_button).addEventListener('click', function (event) {
                console.log('button clicked -> input clicked')
                document.getElementById(id_input).click();
            });

            // bind input change event to flow upload
            document.getElementById(id_input).addEventListener('change', function (event) {
                // check file size or type here
                console.log(event.target.files[0]);

                // add file to flow and upload
                flow.addFile(event.target.files[0]);
                flow.upload();  // or triggered by event

                // reset input value
                event.target.value = '';
            });
        },
    },
});