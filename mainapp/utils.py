from datetime import datetime, timedelta
from mainapp.models import EventCategory, Event, EventCollection, EventDate


def kid_events():
    kid_categories = ['0+', '6+', '12+']
    return Event.objects.filter(category__name__in=kid_categories, is_active=True)


def weekend_events():
    current_week_day = datetime.today().weekday()
    nearest_weekend = datetime.date(datetime.today() + timedelta(5 - current_week_day))
    return Event.objects.filter(dates__date__range=(nearest_weekend, nearest_weekend + timedelta(2)), is_active=True)


def free_events():
    return Event.objects.filter(is_free=True, is_active=True)


def health_events():
    return Event.objects.filter(is_active=True, category__name__in=['Спорт', 'Цирк'])
