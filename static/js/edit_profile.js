document.addEventListener('DOMContentLoaded', function () {
    // Обработка формы регистрации
    document.getElementById('profile-form').addEventListener('edit-button', function (e) {
        e.preventDefault();

        const login = document.getElementById('login').value;
        const first_name = document.getElementById('first_name').value;
        const name = document.getElementById('name').value;
        const second_name = document.getElementById('second_name').value;
        const phone = document.getElementById('phone').value;
        const email = document.getElementById('email').value;

        const data = {
            "login": login,
            "first_name": first_name,
            "name": name,
            "second_name": second_name,
            "phone": phone,
            "email": email
        };

        fetch('http://127.0.0.1:5000/edit_profile', {
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
});
