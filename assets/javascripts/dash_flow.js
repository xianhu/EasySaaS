/**
 * flow object in dash
 * @type {any}
 */

// flow object
const flow = new Flow({
    target: '/upload',
    testChunks: false,
    uploadMethod: 'POST',
    chunkSize: 1024 * 1024,
    simultaneousUploads: 1,
    allowDuplicateUploads: true,
    progressCallbacksInterval: 1000,
});

// define flow events
flow.on('fileAdded', function (file, event) {
    console.log('file added');
    sessionStorage.setItem('id-key-flow', JSON.stringify({
        status: 'fileAdded',
        file_name: file.name,
        _timestamp: new Date().getTime(),
    }));
});

// define flow events
flow.on('fileSuccess', function (file, message) {
    console.log('file success');
    sessionStorage.setItem('id-key-flow', JSON.stringify({
        status: 'fileSuccess',
        file_name: file.name,
        _timestamp: new Date().getTime(),
    }));
});

// define flow events
flow.on('fileError', function (file, message) {
    console.log('file error');
    sessionStorage.setItem('id-key-flow', JSON.stringify({
        status: 'fileError',
        file_name: file.name,
        _timestamp: new Date().getTime(),
    }));
});

// define flow events
flow.on('fileProgress', function (file) {
    let percent = Math.floor(file.progress() * 100);
    console.log('file progress: ' + percent + '%');
});

console.log("dash_flow.js loaded")