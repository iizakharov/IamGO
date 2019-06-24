from django.db import models


class EventCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(verbose_name='Имя категории', max_length=64, unique=True)
    description = models.TextField(verbose_name='Описание категории', max_length=500, blank=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    def __str__(self):
        return self.name


class EventAgent(models.Model):
    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'

    name = models.CharField(verbose_name='Имя агента', max_length=64, unique=True)
    info = models.TextField(verbose_name='Описание агента', max_length=500, blank=True)
    is_active = models.BooleanField(verbose_name='Активен', default=True)

    def __str__(self):
        return self.name


class EventLocation(models.Model):
    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Площадки'

    name = models.CharField(verbose_name='Название площадки', max_length=64, unique=True)
    location = models.CharField(verbose_name='Адрес площадки', max_length=500, blank=True)

    def __str__(self):
        return self.name


class EventDate(models.Model):
    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'

    date = models.DateField(verbose_name='Дата')


class Event(models.Model):
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    agent = models.ForeignKey(EventAgent, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название события', max_length=128)
    description = models.CharField(verbose_name='Краткое описание события', max_length=60, blank=True)
    body_text = models.TextField(verbose_name='Описание события', blank=True)
    location = models.ManyToManyField(EventLocation)
    date = models.ManyToManyField(EventDate, verbose_name='Дата')
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2, default=0)
    is_free = models.BooleanField(verbose_name='Бесплатное', default=True)
    is_active = models.BooleanField(verbose_name='Активное', default=True)
    image = models.ImageField(upload_to='products_images', blank=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class EventGallery(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery')
