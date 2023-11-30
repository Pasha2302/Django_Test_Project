
from django.forms import model_to_dict
from django.shortcuts import render

from django.http import HttpRequest, Http404, JsonResponse
from django.shortcuts import redirect

from asgiref.sync import sync_to_async, async_to_sync
from django.utils.decorators import method_decorator
from django.views import View

from app_test.models import SlotCatalog
from django.contrib.auth.views import LoginView

from .my_decorators import login_required as log_req
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist


class CustomLoginView(LoginView):
    template_name ='app_test/registration/login.html'

    async def form_invalid(self, form):
        # Дополнительные действия (при неверных данных формы)
        messages.error(self.request, 'Неправильный логин или пароль')
        # Вызываем метод form_invalid родительского класса для стандартной обработки
        return super().form_invalid(form)


@log_req
async def profile_view(request):
    # Редирект на главную страницу
    return redirect(index)


async def task_sleep():
    print("Ожидание 30 сек ...")
    await asyncio.sleep(60)
    print("\nЯ проснулся !")


@log_req
async def index(request: HttpRequest):
    asyncio.create_task(task_sleep())
    await asyncio.sleep(0)
    return render(request, "app_test/TEST.html")


from .Tools import toolbox
from .Tools import SlotCatalogDb

slots_data: None  = None
db_slot_catalog: SlotCatalogDb = SlotCatalogDb(
    host='127.0.0.1', port=3306, user='pavelpc', password='1234', database='slotCatalogDjango'
)


@toolbox.time_it_async
async def get_all_data_db():
    query_db = "SELECT id, name_slot, provider, slug FROM app_test_slotcatalog"
    return await db_slot_catalog.execute_query(query_db, fetch=True)

@toolbox.time_it_async
async def get_all_data_db_orm():
    return await sync_to_async(list)(SlotCatalog.objects.all().values('id', 'name_slot', 'provider', 'slug'))

class SlotsListView(View):
    template_name = "app_test/test_paginator.html"


    @method_decorator(log_req)
    @toolbox.time_it_async
    async def get(self, request: HttpRequest):
        global slots_data
        page_number = request.GET.get("page", 1)

        # if not slots_data:
        await db_slot_catalog.connect()
        print("\nЗапрашиваю данные из базы [SlotCatalog]")
        # slots_data = await SlotCatalog.objects.values('id', 'name_slot', 'provider', 'slug')
        # slots_data = await get_all_data_db_orm()
        slots_data = await get_all_data_db()


        # paginator = Paginator(slots_data.order_by('id'), 24)
        paginator = Paginator(slots_data, 24)

        range_pages = paginator.get_elided_page_range(number=page_number, on_each_side=1, on_ends=1)
        try:
            page_obj = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            raise Http404()

        context = {"page_obj_slots": page_obj, 'range_pages': range_pages}
        return render(request, self.template_name, context=context)


@log_req
async def one_slot(request: HttpRequest, slug_slot=None):
    print(f"One Slot: {slug_slot}, request.GET: {request.GET}")

    # sync_to_async по умолчанию работает в "потоко-чувствительном" режиме. (избегая состояния гонки.)
    # thread_sensitive: bool = True (блокирует основной поток.)
    # data_slot = await sync_to_async(get_object_or_404)(SlotCatalog, slug=slug_slot)

    try:
        data_slot = await SlotCatalog.objects.aget(slug=slug_slot)
    except ObjectDoesNotExist: raise Http404
    print(f"{data_slot=}")
    # Преобразуем объект в словарь
    slot_dict = model_to_dict(data_slot)

    del slot_dict['slug']
    context = {"data_slot": slot_dict}
    return render(request, template_name="app_test/one_slot.html", context=context)

# ******************************************************************************************************* *


async def load_more(request):
    # Ваш код для загрузки следующих данных
    # Пример возврата данных в формате JSON
    count = request.GET.get('count', 0)
    count = int(count)

    async def get_new_data():
        return [f'Новые данные {count + i}' for i in range(1, 50)]

    count += 10

    data = {
        'response': await get_new_data(),  # Замените на реальные данные
        'next_data_url': f'/load_more?count={count}',  # Замените на реальный URL
    }

    return JsonResponse(data)


def test_scroll(request: HttpRequest):
    return render(request, template_name="app_test/test_scroll.html")


def handler404(request: HttpRequest, exception):
    print("\nHandler 404")
    return render(request, 'app_test/404.html', status=404)

# ============================================================================================================== #
import asyncio
import time
from aiohttp import ClientSession
import aiohttp

# from .create_connection_pool import CreatePool
# from typing import List, Dict
# from asyncpg import Record

# import psycopg2

# conn_info = "dbname=products user=postgres password=password host=127.0.0.1"
# db = psycopg2.connect(conn_info)

pool = None



# async def brands(request):
#     cur = db.cursor()
#
#     brand_query = 'SELECT brand_id, brand_name FROM brand'
#     cur.execute(brand_query)
#     rows = cur.fetchall()
#     # await asyncio.sleep(10)
#     cur.close()
#     result_as_dict: List[Dict] = [{'brand_id': row[0], 'brand_name': row[1]} for row in rows]
#
#     return HttpResponse(f"<h2> {id(asyncio.get_running_loop())}</h2> <p><b>{result_as_dict}</p>")


async def get_url_details(session: ClientSession, url: str):
    start_time = time.time()
    response = await session.get(url)
    response_body = await response.text()
    end_time = time.time()
    return {'status': response.status,
            'time': f"{(end_time - start_time):.4f}",
            'body_length': len(response_body),
            'loop': id(asyncio.get_running_loop())
            }


async def make_requests(url: str, request_num: int):
    async with aiohttp.ClientSession() as session:
        requests = [get_url_details(session, url) for _ in range(request_num)]
        results = await asyncio.gather(*requests, return_exceptions=True)
        failed_results = [str(result) for result in results if isinstance(result, Exception)]
        successful_results = [result for result in results if not isinstance(result, Exception)]
        return {'failed_results': failed_results, 'successful_results': successful_results}


async def requests_view(request):
    url: str = request.GET['url']
    request_num: int = int(request.GET['request_num'])
    context = await make_requests(url, request_num)
    return render(request, 'async_api/requests.html', context)

# ==================================================================================================================== #


from functools import partial
from django.http import HttpResponse



def sleep(seconds: int):
    time.sleep(seconds)


async def sync_to_async_view(request):
    # Книга, страница - 277
    start_time = time.time()

    sleep_time: int = int(request.GET['sleep_time'])
    num_calls: int = int(request.GET['num_calls'])
    thread_sensitive: bool = request.GET['thread_sensitive'] == 'True'

    function = sync_to_async(partial(sleep, sleep_time), thread_sensitive=thread_sensitive)
    await asyncio.gather(*[function() for _ in range(num_calls)])

    time_done = f"{(time.time() - start_time):.4f}"
    return HttpResponse(f'<h3>Время загрузки страницы: <p> {time_done} sec. </p> </h3>')


def requests_view_sync(request):
    url: str = request.GET['url']
    request_num: int = int(request.GET['request_num'])
    context = async_to_sync(partial(make_requests, url, request_num))()
    return render(request, 'async_api/requests.html', context)
