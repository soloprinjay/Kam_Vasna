document.getElementById('contact-form').addEventListener('submit', function (event) {
    event.preventDefault();

    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    // Prepare the data to send
    const data = {
        name: name,
        email: email,
        subject: subject,
        message: message
    };

    // Get the CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Get the form action URL (OPTION 2: You can now safely hardcode or pass from HTML)
    const url = '/contact/';  // ✅ replace with actual URL or use data-url pattern from Option 1

    // Make the AJAX request
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const alertDiv = document.getElementById('alert');
        if (data.status === 'success') {
            alertDiv.classList.remove('hidden', 'bg-red-500');
            alertDiv.classList.add('bg-green-500');
            alertDiv.innerText = data.message;
        } else {
            alertDiv.classList.remove('hidden', 'bg-green-500');
            alertDiv.classList.add('bg-red-500');
            alertDiv.innerText = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
