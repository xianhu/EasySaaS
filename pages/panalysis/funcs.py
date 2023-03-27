# _*_ coding: utf-8 _*_

"""
functions module
"""


def get_js_flow(id_div_input, id_button_upload, id_storage):
    """
    get js according to flow.js
    """
    return f"""
        // add input to div
        var div = document.getElementById('{id_div_input}');
        div.innerHTML="<input id='id-input-file' type='file' name='file' style='display:none;'/>";

        // define flow instance
        var flow = new Flow({{
            target: '/upload',
            testChunks: false,
            uploadMethod: 'POST',
            chunkSize: 1024 * 1024,
            simultaneousUploads: 1,
            allowDuplicateUploads: true,
            progressCallbacksInterval: 1000,  
        }});

        // define flow events
        flow.on('fileAdded', function (file, event) {{ 
            console.log('file added');
            sessionStorage.setItem('{id_storage}', JSON.stringify({{
                status: 'fileAdded',
                file_name: file.name,
                _timestamp: new Date().getTime(),
            }}));
        }});

        // define flow events
        flow.on('fileSuccess', function (file, message) {{
            console.log('file success');
            sessionStorage.setItem('{id_storage}', JSON.stringify({{
                status: 'fileSuccess',
                file_name: file.name,
                _timestamp: new Date().getTime(),                
            }}));
        }});

        // define flow events
        flow.on('fileError', function (file, message) {{
            console.log('file error');
            sessionStorage.setItem('{id_storage}', JSON.stringify({{
                status: 'fileError',
                file_name: file.name,
                _timestamp: new Date().getTime(),
            }}));
        }});

        // define flow events
        var output = document.getElementById('');
        flow.on('fileProgress', function (file) {{
            let percent = Math.floor(file.progress() * 100);
            console.log('file progress: ' + percent + '%');
            if (output) {{
                output.innerHTML = 'progress: ' + percent + '%';
            }}
        }});
        
        // bind button click event to input click
        document.getElementById('{id_button_upload}').addEventListener('click', function() {{
            document.getElementById('id-input-file').click();
        }});

        // bind input change event to flow upload
        document.getElementById('id-input-file').addEventListener('change', function(event) {{
            flow.addFile(event.target.files[0]);
            flow.upload();
        }});
    """
