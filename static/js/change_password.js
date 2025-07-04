document.getElementById('change-password-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-new-password').value;

    const response = await fetch('/users/change-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword,
            confirm_password: confirmPassword,
        }),
    });

    const data = await response.json();

    if (response.ok) {
        showSuccess(data.message || "पासवर्ड सफलतापूर्वक बदल दिया गया।");
        setTimeout(() => {
            window.location.href = "/";  // Redirect to dashboard:home
        }, 1000);
    } else {
        showError(data.message || "एक त्रुटि हुई। कृपया पुनः प्रयास करें।");
    }
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