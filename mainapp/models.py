import os
from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{uuid4().hex}.{ext}'

        return os.path.join(self.path, filename)


path_and_rename = PathAndRename("static/img/tmp")


class EventCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    name = models.CharField(verbose_name='Имя категории', max_length=64, unique=True)
    description = models.CharField(verbose_name='Краткое описание категории', max_length=128, blank=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    def __str__(self):
        return self.name


class EventAgent(models.Model):
    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'
        ordering = ['name']

    name = models.CharField(verbose_name='Имя агента', max_length=64, unique=True)
    description = models.CharField(verbose_name='Краткое описание агента', max_length=128, blank=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    def __str__(self):
        return self.name


class EventLocation(models.Model):
    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'
        ordering = ['name']

    name = models.CharField(verbose_name='Название площадки', max_length=64, unique=True)
    location = models.CharField(verbose_name='Адрес площадки', max_length=500)
    google_map = models.CharField(verbose_name='Метка яндекс карты', max_length=500)

    def __str__(self):
        return self.name


class EventCollection(models.Model):
    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'
        ordering = ['name']

    name = models.CharField(verbose_name='Имя подборки', max_length=255, unique=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)
    image = models.ImageField(upload_to=path_and_rename, blank=True)

    def __str__(self):
        return {self.name}


class EventManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (
                    Q(name__icontains=query) |
                    Q(description__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Event(models.Model):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['name']

    category = models.ManyToManyField(EventCategory, verbose_name='Категория')
    agent = models.ForeignKey(EventAgent, on_delete=models.CASCADE, verbose_name='Организатор')
    name = models.CharField(verbose_name='Название события', max_length=128)
    description = models.CharField(verbose_name='Краткое описание события', max_length=128, blank=True)
    body_text = models.TextField(verbose_name='Описание события', blank=True)
    location = models.ManyToManyField(EventLocation, verbose_name='Площадка')
    price = models.DecimalField(verbose_name='Цена от', max_digits=8, decimal_places=2, default=0)
    is_free = models.BooleanField(verbose_name='Бесплатное', default=True)
    is_active = models.BooleanField(verbose_name='Активное', default=True)
    is_hot = models.BooleanField(verbose_name='Популярное', default=False)
    # collections = models.ForeignKey(EventCollection, on_delete=models.CASCADE, verbose_name='Подборки', blank=True,
    #                                 null=True)

    objects = EventManager()

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return f'{self.name}'

    @property
    def get_avatar(self):
        try:
            avatar = self.images.filter(is_avatar=True).first().image.url
        except AttributeError:
            avatar = '/static/img/s372x223_lelingrad.webp'
        return avatar

    @property
    def get_location_url(self):
        try:
            url = self.location.first().google_map
        except AttributeError:
            url = None
        return url

    @property
    def get_location_name(self):
        try:
            return self.location.first().name
        except AttributeError:
            return None

    @property
    def get_dates(self):
        try:
            return self.dates.all()
        except AttributeError:
            return None


class EventGallery(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['image']

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images', verbose_name='Название события')
    image = models.ImageField(
        upload_to=path_and_rename,
        height_field='image_height',
        width_field='image_width',
        verbose_name='Изображение события'
    )
    is_avatar = models.BooleanField(verbose_name='Главное изображение события', default=False)
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default='100')
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default='100')

    def __str__(self):
        return f'{self.event.name}'


class EventDate(models.Model):
    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'
        ordering = ['date']

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='dates', verbose_name='Название события')
    date = models.DateTimeField(verbose_name='Дата события')

    def __str__(self):
        return f'{self.date}'
