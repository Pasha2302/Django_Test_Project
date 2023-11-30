
//
let dataRtp = {minValue: 0, maxValue: 100};
let dataWin = {minValue: 0, maxValue: 300000000};
let checkIframe = null


const filterInput = document.getElementById('filterInput');
const resultsList = document.getElementById('results');
//const socket = new WebSocket('ws://92.53.124.166/ws/test_filter');
//const socket = new WebSocket('ws://127.0.0.1:8000/ws/test_filter/');
const socket = new WebSocket('wss://7966-185-211-158-227.ngrok-free.app/ws/test_filter/');


// Обработка поля ввода названия слота:
filterInput.addEventListener('input', function() {
    // Отправляем введенные данные на сервер
    let query = encodeURIComponent(filterInput.value);

    // Пример отправки данных в формате JSON
    const requestData = { data: query, valueRtp: dataRtp, valueWin: dataWin, checkIframe: checkIframe };
    const requestJson = JSON.stringify(requestData);
    socket.send(requestJson);

});


// Обработка чек-бокса Iframe:
document.addEventListener('DOMContentLoaded', function() {
    let checkbox = document.getElementById('optionIframe');

    checkbox.addEventListener('change', function() {
        if (checkbox.checked) {
              console.log('Чекбокс включен');
              checkIframe = true
              // Здесь можно выполнить нужные действия, когда чекбокс включен
        } else {
            checkIframe = null
            console.log('Чекбокс выключен');
        }
        // Здесь можно выполнить нужные действия, когда чекбокс выключен
        let query = encodeURIComponent(filterInput.value);
        const requestData = { data: query, valueRtp: dataRtp, valueWin: dataWin, checkIframe: checkIframe };
        const requestJson = JSON.stringify(requestData);
        socket.send(requestJson);
    });
});



// Обрабатываем событие от сервера
socket.onmessage = function(event) {
    const dataJsonServer = JSON.parse(event.data);
    const dataJsonSlots = dataJsonServer.data_slots

    // Очищаем текущий список
    resultsList.innerHTML = '';

    count_row = 1
    for (const slot of dataJsonSlots) {
        // Создаем элемент li
        const li = document.createElement('li');

        // Создаем элемент a
        const link = document.createElement('a');
        link.href = slot.url_card;  // Устанавливаем URL-адрес
        link.textContent = `[${count_row}] ${slot.name_card}`;  // Устанавливаем текст ссылки

        // Добавляем элемент a в элемент li
        li.appendChild(link);

        // Добавляем элемент li в список
        resultsList.appendChild(li);
        count_row = count_row + 1
    }
};


document.addEventListener('DOMContentLoaded', function() {
    let rangeInput = document.getElementById('range-input');
    let rangeInput2 = document.getElementById('range-input2');
    let rangeValues = document.getElementById('range-values');

    rangeInput.addEventListener('input', updateRangeValues);
    rangeInput2.addEventListener('input', updateRangeValues);

    rangeInput.addEventListener('change', sendDataRtp);
    rangeInput2.addEventListener('change', sendDataRtp);

    function updateRangeValues() {
        let minValue = parseInt(rangeInput.value);
        let maxValue = parseInt(rangeInput2.value);

        if (minValue > maxValue) {
            rangeInput.value = maxValue;
            minValue = maxValue;
        }

        rangeValues.textContent = minValue + ' - ' + maxValue;
//        console.log(`RTP: (${minValue}, ${maxValue})`)

        dataRtp.minValue = minValue;
        dataRtp.maxValue = maxValue;
    }

    function sendDataRtp() {
        // Пример отправки данных в формате JSON
        let query = encodeURIComponent(filterInput.value);
        const requestData = { data: query, valueRtp: dataRtp, valueWin: dataWin, checkIframe: checkIframe };
        const requestJson = JSON.stringify(requestData);
        socket.send(requestJson);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    let rangeInputMaxWin = document.getElementById('range-input3');
    let rangeInputMaxWin2 = document.getElementById('range-input4');
    let rangeValuesMaxWin = document.getElementById('range-values1');

    rangeInputMaxWin.addEventListener('input', updateRangeValues);
    rangeInputMaxWin2.addEventListener('input', updateRangeValues);

    rangeInputMaxWin.addEventListener('change', sendDataWin);
    rangeInputMaxWin2.addEventListener('change', sendDataWin);

    function updateRangeValues() {
        let maxWinValue = parseInt(rangeInputMaxWin2.value);
        let minWinValue = parseInt(rangeInputMaxWin.value);

        if (minWinValue > maxWinValue) {
            rangeInputMaxWin.value = maxWinValue;
            minWinValue = maxWinValue;
        }

        rangeValuesMaxWin.textContent = minWinValue + ' - ' + maxWinValue;
        // console.log(`Max Win ${minWinValue}, ${maxWinValue}`)

        dataWin.minValue = minWinValue;
        dataWin.maxValue = maxWinValue;
    }

    function sendDataWin() {
        // Пример отправки данных в формате JSON
        let query = encodeURIComponent(filterInput.value);
        const requestData = { data: query, valueRtp: dataRtp, valueWin: dataWin, checkIframe: checkIframe };
        const requestJson = JSON.stringify(requestData);
        socket.send(requestJson);

    }
});


// Отмена клавиатурных событий:
document.addEventListener('DOMContentLoaded', function() {
    let rangeInput = document.getElementById('range-input');
    let rangeInput2 = document.getElementById('range-input2');
    let rangeInput3 = document.getElementById('range-input3');
    let rangeInput4 = document.getElementById('range-input4');

    rangeInput.addEventListener('keydown', preventKeyEvent);
    rangeInput2.addEventListener('keydown', preventKeyEvent);
    rangeInput3.addEventListener('keydown', preventKeyEvent);
    rangeInput4.addEventListener('keydown', preventKeyEvent);

    function preventKeyEvent(event) {
        event.preventDefault();
    }
});


// Делаем input теги не активными какое то время после использования:
document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы полей ввода
    let rangeInput = document.getElementById('range-input');
    let rangeInput2 = document.getElementById('range-input2');
    let rangeInput3 = document.getElementById('range-input3');
    let rangeInput4 = document.getElementById('range-input4');
    let rangeInput5 = document.getElementById('range-input5');
    let rangeInput6 = document.getElementById('range-input6');

    // Добавляем обработчик события change для каждого поля ввода
    rangeInput.addEventListener('change', function() {
        disableInputForSomeTime(rangeInput);
    });

    rangeInput2.addEventListener('change', function() {
        disableInputForSomeTime(rangeInput2);
    });

    rangeInput3.addEventListener('change', function() {
        disableInputForSomeTime(rangeInput3);
    });

    rangeInput4.addEventListener('change', function() {
        disableInputForSomeTime(rangeInput4);
    });

    rangeInput5.addEventListener('change', function() {
        disableInputForSomeTime(rangeInput5);
    });

    rangeInput6.addEventListener('change', function() {
        disableInputForSomeTime(rangeInput6);
    });

    // Функция для временного отключения поля ввода
    function disableInputForSomeTime(inputElement) {
        // Устанавливаем атрибут disabled
        inputElement.disabled = true;

        // Устанавливаем таймер на 3 секунды (или другое нужное вам время)
        setTimeout(function() {
            // Снимаем атрибут disabled
            inputElement.disabled = false;
        }, 3000); // 3000 миллисекунд = 3 секунды
    }
});
