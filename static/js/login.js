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


document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // Important to stop normal form submission

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const rememberMe = document.getElementById('remember-me').checked;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch('/users/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                    remember_me: rememberMe,
                }),
            });

            const data = await response.json();

            if (data.success) {
                showSuccess(data.message || 'लॉगिन सफल!');
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1000);
            } else {
                showError(data.message || 'लॉगिन असफल');
            }
        } catch (error) {
            console.error('Login error:', error);
            showError('कुछ गलत हो गया। कृपया पुनः प्रयास करें।');
        }
    });
});


// document.getElementById('login-form').addEventListener('submit', async function (e) {
//     e.preventDefault();
//
//     const email = document.getElementById('email').value;
//     const password = document.getElementById('password').value;
//     const rememberMe = document.getElementById('remember-me').checked;
//     const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//
//     const response = await fetch("{% url 'users:login-user' %}", {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken
//         },
//         body: JSON.stringify({
//             email: email,
//             password: password,
//             remember_me: rememberMe
//         })
//     });
//
//     const data = await response.json();
//
//     if (data.success) {
//         alert("लॉगिन सफल! Redirecting...");
//         window.location.href = data.redirect_url;
//     } else {
//         alert(data.message);
//     }
// });
