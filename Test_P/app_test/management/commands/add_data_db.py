from django.core.management.base import BaseCommand
from app_test.models import SlotCatalog
from datetime import datetime

from app_test.Tools import toolbox


class Command(BaseCommand):
    help = 'Загрузка данных и установка date_added для SlotCatalog'

    def handle(self, *args, **options):
        slots_data_json = toolbox.download_json_data(path_file="format_data_slots.json")

        for data_slot in slots_data_json:
            # Ваша существующая логика обработки данных здесь

            # Установка date_added на текущую дату и время
            data_slot['date_added'] = datetime.now()

            # Создание нового экземпляра SlotCatalog с использованием auto_now_add
            try:
                slot_instance = SlotCatalog.objects.create(**data_slot)
            except Exception as err_add_db:
                print(f"Error: {err_add_db}\n {data_slot}")
                raise

        self.stdout.write(self.style.SUCCESS('Успешно загружены данные и установлен date_added'))


# python manage.py add_data_db
