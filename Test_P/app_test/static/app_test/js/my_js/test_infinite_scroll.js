var nextDataUrl = "{% url 'load_more' %}";

function loadMore() {
  $('#loading').show();

  if (nextDataUrl === "") {
    $('#loading').hide();
    return;
  }

  $.getJSON(nextDataUrl, function(data) {
    $('#data-list').append(data.response);
    nextDataUrl = data.nextDataUrl;
    $('#loading').hide();
  });
}

$(document).ready(function() {
  // Обработка события прокрутки
  $(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
      loadMore();
    }
  });

  // Вызовем loadMore при загрузке страницы
  loadMore();
});

