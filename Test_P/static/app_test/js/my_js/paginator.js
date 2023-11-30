
function showPageInput(event, pageNumber) {
    var pageInputContainer = document.getElementById('pageInputContainer');
    pageInputContainer.style.display = 'block';

    event.stopPropagation(); // Остановить всплытие события, чтобы избежать конфликта

    // Добавляем слушатель кликов на документ, если вызов произошел не от кнопки "Go"
    if (event.target.tagName !== 'BUTTON' && event.target === goToPageInput) {
        document.addEventListener('click', function handleClick(event) {
            var pageInputContainer = document.getElementById('pageInputContainer');
            var goToPageInput = document.getElementById('goToPageInput');

            // Проверяем, был ли клик на кнопке "Go" или вне блока и вне самого поля ввода
            if (event.target === goToPageInput || (!pageInputContainer.contains(event.target) && event.target !== goToPageInput)) {
                pageInputContainer.style.display = 'none';
                document.removeEventListener('click', handleClick); // Удаляем обработчик после его использования
            }
        });
    }
}

function generateUrl() {
    event.preventDefault();
    let pageInput = document.getElementById('goToPageInput');
    let page = pageInput.value.trim();

    if (page !== "") {
        let baseUrl = window.location.pathname;
//        let url = "{% url 'slots_list' %}?page=" + encodeURIComponent(page);
        let url = "?page=" + encodeURIComponent(page);
        window.location.href = url;
    } else {
        alert('Введите номер страницы.');
    }
}

document.getElementById('goToPageInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        generateUrl();
    }
});
