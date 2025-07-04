document.addEventListener('DOMContentLoaded', function () {
    const signup_form = document.getElementById('signup-form');

    signup_form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const full_name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const password2 = document.getElementById('confirm-password').value;
        const terms = document.getElementById('terms').checked; // Assuming you have a checkbox with id="terms"

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch('/users/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken, // CSRF token for Django security
                },
                body: JSON.stringify({
                    full_name: full_name,
                    email: email,
                    password: password,
                    'confirm-password': password2,
                    terms: terms,
                }),
            });

            const data = await response.json();

            if (data.success) {
                showSuccess(data.message);
                setTimeout(() => {
                    window.location.href = '/users/login/'; // Redirect to login page after success
                }, 1000);
            } else {
                showError(data.message); // Show error message
            }

        } catch (error) {
            console.error('Error:', error);
            showError('कुछ गलत हो गया। कृपया पुनः प्रयास करें।');
        }
    });
});



function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const parent = input.parentElement;
    const showIcon = parent.querySelector('.password-show');
    const hideIcon = parent.querySelector('.password-hide');

    if (input.type === 'password') {
        input.type = 'text';
        showIcon.classList.remove('hidden');
        hideIcon.classList.add('hidden');
    } else {
        input.type = 'password';
        showIcon.classList.add('hidden');
        hideIcon.classList.remove('hidden');
    }
}