function onPageLoadOrRefresh() {
    fileIdCounter = -1;
    eel.reset_files()(function(){});
}

// Set the function to run when the page is loaded or refreshed
window.onload = onPageLoadOrRefresh;

function uploadFiles() {
    document.getElementById('files-for-upload').click();
}

function clearAllFiles() {
    const filesList = document.getElementById('selected-files');
    while (filesList.length > 0) {
        filesList.remove(0);
    };
    fileIdCounter = -1;
    eel.reset_files()(function(){});

}
function clearSelectedFiles() {
    const filesList = document.getElementById('selected-files');
    
    while (filesList.selectedIndex != -1) {
        eel.remove_file_content(filesList.selectedIndex)(function(){});
        filesList.remove(filesList.selectedIndex);
    }
}
function moveFilesUp() {
    const filesList = document.getElementById('selected-files');
    
    for (let i = 1; i < filesList.length; i++) {
        var option = filesList.options[i];
        var previous_option = filesList.options[i-1];
        if (option.selected && !previous_option.selected) {
            filesList.add(option, i-1);
            filesList.add(previous_option, i);
        };
    };
}
function moveFilesDown() {
    const filesList = document.getElementById('selected-files');
    
    for (let i = filesList.length-1; i>0; i--) {
        var option = filesList.options[i-1];
        var next_option = filesList.options[i];
        if (option.selected && !next_option.selected) {
            filesList.add(option, i);
            filesList.add(next_option, i-1);
        };
    };
}

function mergeFiles() {
    const filesList = document.getElementById('selected-files').options;
    const filesIdsList = new Array(filesList.length)

    for (let i = 0; i < filesList.length; i++) {
        filesIdsList[i] = filesList[i].value;
    }
    const includeBookmarks = document.getElementById('include-bookmarks').checked;
    eel.merge_pdf_files_py(filesIdsList, includeBookmarks)(function(result) {
        download(result[1], 'MERGED_PDF.pdf');
    });
}

function download(contentBase64, filename) {
    var bytes = base64ToArrayBuffer(contentBase64);

    var blob = new Blob([bytes], {type: "application/pdf"});

    //creating an invisible element
    var element = document.createElement('a');
    element.href = window.URL.createObjectURL(blob);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function base64ToArrayBuffer(base64) {
    var binaryString = atob(base64);
    var binaryLen = binaryString.length;
    var bytes = new Uint8Array(binaryLen);
    for (var i = 0; i < binaryLen; i++) {
       var ascii = binaryString.charCodeAt(i);
       bytes[i] = ascii;
    }
    return bytes;
}

function readFileAsBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            const base64String = reader.result.split(',')[1];
            resolve(base64String);
        };
        reader.onerror = () => {
            reject(reader.error);
        };
        reader.readAsDataURL(file);
    });
}
async function loadFiles() {

    const filesUploadList = document.getElementById('files-for-upload').files;
    const listFiles = document.getElementById('selected-files');

    for (let i = 0; i < filesUploadList.length; i++) {
        var file = filesUploadList[i];
        var optionElement = document.createElement('option');
        optionElement.textContent = file.name;
        optionElement.value = ++fileIdCounter;
        try {
            const base64String = await readFileAsBase64(file, optionElement);
            eel.store_file_content(fileIdCounter, base64String, file.name)(function () {});
        } catch (error) {
            console.error('Error reading file:', error);
        }
        listFiles.appendChild(optionElement);

    };
}