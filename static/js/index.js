document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const queryForm = document.getElementById('query-form');
    const chatBox = document.getElementById('chat-box');

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(uploadForm);

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            chatBox.innerHTML += '<div class="response-message">' + data + '</div>';
            chatBox.scrollTop = chatBox.scrollHeight;
            uploadForm.style.display = 'none';
            queryForm.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    });

    queryForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const searchText = document.getElementById('search_text').value;
        chatBox.innerHTML += '<div class="user-message"><b>User:</b> ' + searchText + '</div>';
        document.getElementById('search_text').value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ search_text: searchText })
        })
        .then(response => response.text())
        .then(data => {
            chatBox.innerHTML += '<div class="response-message"><b>System:</b> ' + data.replace("OpenAI", "Dreamboat") + '</div>';
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => console.error('Error:', error));
    });
});