from django.contrib import admin

# Register your models here.
from .models import SlotCatalog


@admin.register(SlotCatalog)
class GameSlots(admin.ModelAdmin):
    list_display = ('id', 'name_slot', 'provider', 'slug', 'date_added')
    list_display_links = ('id', 'name_slot')

