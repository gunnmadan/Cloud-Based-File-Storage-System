// script.js

// Upload File
const uploadForm = document.getElementById('uploadForm');
uploadForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('uploadStatus').innerText = data.message;
        loadFiles();
    })
    .catch(err => console.error('Upload failed:', err));
});

// Load Files
function loadFiles() {
    fetch('/files')
    .then(res => res.json())
    .then(files => {
        const fileList = document.getElementById('fileList');
        fileList.innerHTML = '';
        files.forEach(file => {
            fileList.innerHTML += `
                <tr>
                    <td>${file.filename}</td>
                    <td><a href="/download/${file.id}" target="_blank">Download</a></td>
                    <td><button onclick="shareFile(${file.id})">Share</button></td>
                </tr>`;
        });
    })
    .catch(err => console.error('Error loading files:', err));
}

// Share File
function shareFile(fileId) {
    fetch(`/share/${fileId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'public@link.com' }) // Replace with actual user email if needed
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('shareLink').value = data.share_link;
    })
    .catch(err => console.error('Error sharing file:', err));
}

// Initial load
loadFiles();
