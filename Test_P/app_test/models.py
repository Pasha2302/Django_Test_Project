from datetime import datetime

from django.db import models
from django.utils.text import slugify
from django.db.models.manager import BaseManager, Manager, QuerySet


class CustomManager(BaseManager.from_queryset(QuerySet)):
    data = None
    def custom_method(self) -> int:
        return self.data


class SlotCatalog(models.Model):
    # id = models.IntegerField(primary_key=True)
    name_slot = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True, default=None, max_length=255)

    url_slot = models.URLField()
    iframe_game_url = models.URLField(null=True, max_length=1000)
    provider = models.CharField(max_length=255, null=True)

    release_date = models.DateField(null=True)
    wide_release_date = models.DateField(null=True)

    end_date = models.DateField(null=True, blank=True)
    game_type = models.CharField(max_length=255, null=True)
    rtp = models.FloatField(null=True)
    volatility = models.CharField(max_length=255, null=True)
    hit_frequency = models.FloatField(null=True)
    max_win = models.FloatField(null=True)
    min_bet = models.FloatField(null=True)
    max_bet = models.FloatField(null=True)
    layout = models.CharField(max_length=255, null=True)
    betways = models.FloatField(null=True)
    features = models.TextField(null=True)
    theme = models.CharField(max_length=255, null=True)
    objects_slot = models.CharField(max_length=255, null=True)

    genre = models.CharField(max_length=255, null=True)
    other_tags = models.CharField(max_length=255, null=True)
    technology = models.CharField(max_length=255, null=True)
    game_size = models.FloatField(null=True)
    last_update = models.DateField(null=True)
    blog_articles = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # objects: QuerySet = models.Manager()
    objects: QuerySet = CustomManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_slot)
        if not self.date_added:
            self.date_added = datetime.now()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name_slot
