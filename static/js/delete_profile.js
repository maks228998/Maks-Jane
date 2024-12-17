document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    const message = document.getElementById('message');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартную отправку формы

        const password = document.getElementById('password').value;
        const password2 = document.getElementById('password2').value;

        if (!password || !password2) {
            message.textContent = 'Пароль отсутствует. Пожалуйста, введите пароль.';
            message.style.color = 'red';
            return;
        }

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.error);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                message.textContent = data.error;
                message.style.color = 'red';
            } else {
                message.textContent = 'Аккаунт успешно удален!';
                message.style.color = 'green';
                // Перенаправление на страницу логина
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            message.textContent = error.message || 'Произошла ошибка при отправке запроса.';
            message.style.color = 'red';
        });
    });
});
