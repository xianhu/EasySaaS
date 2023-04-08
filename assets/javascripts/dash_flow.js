/**
 * flow object in dash
 * @type {any}
 */
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

// define flow events
flow.on('fileAdded', function (file) {
    sessionStorage.setItem('id-storage-flow', JSON.stringify({
        status: 'fileAdded',
        file_name: file.name,
        _timestamp: new Date().getTime(),
    }));
    console.log('file added');
});

// define flow events
flow.on('fileProgress', function (file) {
    let percent = Math.floor(file.progress() * 100);
    // sessionStorage.setItem('id-storage-flow', JSON.stringify({
    //     status: 'fileProgress',
    //     file_name: file.name,
    //     percent: percent,
    //     _timestamp: new Date().getTime(),
    // }));
    console.log('file progress: ' + percent + '%');
});

// define flow events
flow.on('fileSuccess', function (file, message) {
    sessionStorage.setItem('id-storage-flow', JSON.stringify({
        status: 'fileSuccess',
        file_name: file.name,
        _timestamp: new Date().getTime(),
    }));
    console.log('file success', message);
});

// define flow events
flow.on('fileError', function (file, message) {
    sessionStorage.setItem('id-storage-flow', JSON.stringify({
        status: 'fileError',
        file_name: file.name,
        _timestamp: new Date().getTime(),
    }));
    console.log('file error', message);
});
