document.getElementById('image').addEventListener('change', function() {
    const fileName = this.files[0] ? this.files[0].name : 'Choose an image';
    document.getElementById('file-label').textContent = fileName;
});

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = `Prediction: ${data.prediction}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'Error occurred while predicting.';
    });
});
