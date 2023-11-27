import json
import asyncio
from urllib.parse import unquote

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class ChatConsumerTest(WebsocketConsumer):
    def connect(self):
        print("\nCONNECT Web Socket [ChatConsumerTest]")
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        try:
            current_loop = asyncio.get_running_loop()
            current_loop = id(current_loop)
        except RuntimeError:
            print("! RuntimeError !")
            current_loop = 'No ...'

        text_data_json = json.loads(text_data)
        print(f"{text_data_json=}")
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": f"{message} / Current Loop ID: {current_loop}"}))



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("\nCONNECT Web Socket [ChatConsumer]")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        try:
            current_loop = asyncio.get_running_loop()
            current_loop = id(current_loop)
        except RuntimeError:
            print("! RuntimeError !")
            current_loop = 'No ...'

        text_data_json = json.loads(text_data)
        print(f"{text_data_json=}")
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": f"{message} / Current Loop ID: {current_loop}"}))


# ==================================================================================================================== #
from .Tools import SlotCatalogDb
from .Tools import toolbox
from django.utils.text import slugify
def check_is_numbers(string: str):
    if string.isdigit(): string = float(string)
    else: string = 0.0
    return string


class FilterEndpoint(AsyncWebsocketConsumer):
    async def connect(self):
        print("\nCONNECT Web Socket [FilterEndpoint]")
        await self.accept()

    async def disconnect(self, close_code):
        pass


    @toolbox.time_it_async
    async def receive(self, text_data=None, bytes_data=None):
        db_slot_catalog: SlotCatalogDb = SlotCatalogDb(host='127.0.0.1', port=3306, user='pavelpc', password='1234')

        await db_slot_catalog.connect()

        client_data_json = json.loads(text_data)
        query_frame = ''

        iframe_is = client_data_json['checkIframe']
        print(type(client_data_json), client_data_json)
        # Декодирование URL-кодированных данных
        query_name_card = unquote(client_data_json['data'])
        # query_name_card = client_data_json['data']
        inp_data_rtp: dict = client_data_json['valueRtp']
        inp_data_win: dict = client_data_json['valueWin']
        # print(f"[WebSocket] QUERY: {query_name_card}")

        if len(query_name_card) < -3:
            await self.send(text_data=json.dumps({"data_slots": []}))

        else:
            if query_name_card:
                query_name_card = f'WHERE name_card LIKE "%{query_name_card}%"'
            else:
                query_name_card = "WHERE id"

            if iframe_is: query_frame = " AND iframe_game_url IS NOT NULL AND iframe_game_url <> ''"
            input_query = f'''
                    SELECT url_card, name_card, rtp, max_win
                    FROM slot_catalog_all_slot
                    {query_name_card}{query_frame}
                '''
            try:
                data_slots = await db_slot_catalog.execute_query(query=input_query, fetch=True)
            except Exception as error_db:
                print(f"\nERROR_DB: {error_db}")

            # print(data_slots)
            output_data_slots = []
            for data_slot in data_slots:
                rtp: float = check_is_numbers(data_slot.get('rtp'))
                max_win: float = check_is_numbers(data_slot.get('max_win'))

                if (float(inp_data_rtp['minValue']) <= rtp <= float(inp_data_rtp['maxValue'])) \
                        and (float(inp_data_win['minValue']) <= max_win <= float(inp_data_win['maxValue'])):
                    # print({
                    #     'data_server': {
                    #         'servRtp': rtp,
                    #         'inpRtpMin': float(inp_data_rtp['minValue']),
                    #         'inpRtpMax': float(inp_data_rtp['maxValue'])
                    #     }
                    # })
                    data_slot['url_card'] = f"/slots/{slugify(data_slot['name_card'])}"
                    output_data_slots.append(data_slot)

            await self.send(text_data=json.dumps({"data_slots": output_data_slots}))