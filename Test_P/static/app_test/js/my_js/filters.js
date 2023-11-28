

function validateForm() {
    // Получение данных из формы
    const searchInput = document.getElementById('searchInput').value;
    const option1 = document.getElementById('option1').checked;
    const option2 = document.getElementById('option2').checked;

    // Проверка условий
    if (!searchInput) {
        alert('Заполните все обязательные поля!');
        return false; // Отменить отправку формы
    }

    // Если все в порядке, форма будет отправлена
    return true;
}


async function submitForm() {
    const searchInputValue = document.getElementById('searchInput').value;

    if (!searchInputValue) {
        alert('Введите значение для поиска');
        return;
    }
    const formData = new FormData();
    formData.append('searchInput', searchInputValue);
    try {
        const response = await fetch('/filters/', {
            method: 'POST',
            body: formData,
            headers: {'X-CSRFToken': csrf_token},
        });

        if (response.ok) {
            // Просто перезагрузит страницу, если ответ успешен
            location.reload();
        } else {
            const errorText = await response.text(); // Получить текст ошибки
            console.error('Ошибка при запросе на сервер:', response.status, errorText);
        }
    } catch (error) {
        console.error('Ошибка при выполнении запроса:', error);
    }
}

