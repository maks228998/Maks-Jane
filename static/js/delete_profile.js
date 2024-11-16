document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('login-form').addEventListener('submit', function (e) {
        e.preventDefault();

        const login = document.getElementById('login').value;
        const password = document.getElementById('password').value;

        const data = {
            "login": login,
            "password": password
        };

        fetch('http://127.0.0.1:5000/delete_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            alert('Error:', error);
            console.error('Error:', error);
        });
    });

    const registerButton = document.getElementById('register-button');
    if (registerButton) {
        registerButton.addEventListener('click', function () {
            window.location.href = 'http://127.0.0.1:5000/register'; // Укажите правильный маршрут
        });
    }
});