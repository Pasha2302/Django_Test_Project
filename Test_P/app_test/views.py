from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404

from django.http import HttpRequest
from django.shortcuts import redirect

from app_test.models import SlotCatalog


async def index(request: HttpRequest):
    return render(request, "app_test/TEST.html")


async def room(request: HttpRequest, room_name=None):
    print(f"ROOM: {room_name=}")
    return render(request, "app_test/room.html", {"room_name": room_name})


async def one_slot(request: HttpRequest, slug_slot=None):
    print(f"One Slot: {slug_slot}, request.GET: {request.GET}")

    # sync_to_async по умолчанию работает в "потоко-чувствительном" режиме. (избегая состояния гонки.)
    # thread_sensitive: bool = True (блокирует основной поток.)
    data_slot = await sync_to_async(get_object_or_404)(SlotCatalog, slug=slug_slot)
    # Преобразуем объект в словарь
    slot_dict = model_to_dict(data_slot)

    del slot_dict['slug']
    context = {"data_slot": slot_dict}
    return render(request, template_name="app_test/one_slot.html", context=context)



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
from asgiref.sync import sync_to_async, async_to_sync


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
