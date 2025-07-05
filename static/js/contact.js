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
        if (data.status === 'success') {
            showSuccess(data.message);
            document.getElementById('name').value = "";
            document.getElementById('email').value = "";
            document.getElementById('subject').value = "";
            document.getElementById('message').value = "";
        } else {
            showError(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
