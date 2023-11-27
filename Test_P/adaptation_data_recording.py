from datetime import datetime, timezone
from decimal import Decimal

from django.utils.text import slugify
import re
from app_test.Tools import toolbox


def format_key_objects(data_slot):
    new_key = 'objects_slot'
    data_slot[new_key] = data_slot['objects']
    del data_slot['objects']


def format_key_url_card(data_slot):
    new_key = 'url_slot'
    data_slot[new_key] = data_slot['url_card']
    del data_slot['url_card']


def format_key_name_card(data_slot):
    new_key = 'name_slot'
    data_slot[new_key] = data_slot['name_card']
    del data_slot['name_card']


def format_empty(data_slot):
    for key in data_slot:
        if isinstance(data_slot[key], str):
            if not data_slot[key] or data_slot[key].strip().lower() == 'N/A'.lower():
                data_slot[key] = None


def check_is_numbers(data_slot: dict):
    float_keys = ['max_win', 'min_bet', 'max_bet', 'betways']
    for key in data_slot:
        if key in float_keys:
            new_value_int = re.search(r"\d+", data_slot[key])
            if new_value_int:
                data_slot[key] = float(new_value_int.group())
            else: data_slot[key] = 0.0


def main():
    new_data_list = []
    check_slug = set()
    slots_data_json: list[dict] = toolbox.download_json_data(path_file="slot_catalog_unique_new.json")

    for data_slot in slots_data_json:
        new_data_dict = {"model": "app_test.slotcatalog", "fields": None}
        if data_slot.get('id'):
            del data_slot['id']

        check_is_numbers(data_slot)
        format_key_objects(data_slot)
        format_key_url_card(data_slot)
        format_key_name_card(data_slot)
        format_empty(data_slot)

        # Преобразование значения даты перед сохранением
        for date_field in ['release_date', 'wide_release_date', 'last_update', 'end_date']:
            value = data_slot.get(date_field)
            if value:
                try:
                    # Попробуйте разные форматы даты
                    data_slot[date_field] = datetime.strptime(value, '%Y-%m-%d').strftime('%Y-%m-%d')
                except ValueError:
                    try:
                        # Попробуйте другой формат даты
                        date_obj = datetime.strptime(value, '%d/%m/%Y')
                        # Преобразуйте дату в нужный формат
                        data_slot[date_field] = date_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        try:
                            # Попробуйте другой формат даты
                            date_obj = datetime.strptime(value, '%d-%m-%Y')
                            # Преобразуйте дату в нужный формат
                            data_slot[date_field] = date_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            # Если не удалось преобразовать, установим текущую дату
                            data_slot[date_field] = datetime.now(timezone.utc).strftime('%Y-%m-%d')
                            print(data_slot[date_field])


        if data_slot['name_slot'] == 'Halloween Horrors Megaways':
            print(data_slot)
        if slugify(data_slot['name_slot']) not in check_slug:
            check_slug.add(slugify(data_slot['name_slot']))
            data_slot['slug'] = slugify(data_slot['name_slot'])

            # new_data_dict['fields'] = data_slot
            # new_data_list.append(new_data_dict)
            new_data_list.append(data_slot)

    toolbox.save_json_data(json_data=new_data_list, path_file='format_data_slots.json')


if __name__ == '__main__':
    main()