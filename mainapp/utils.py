from datetime import datetime, timedelta

from mainapp.models import Event


def get_weekends_dates():
    current_week_day = datetime.today().weekday()
    nearest_weekend = datetime.date(datetime.today() + timedelta(5 - current_week_day))
    return {'first_date': nearest_weekend.strftime('%d.%m.%Y'),
            'last_date': (nearest_weekend + timedelta(1)).strftime('%d.%m.%Y')}


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


def get_filter_events(pk=None, begin_date=None, end_date=None, is_active=True):
    if begin_date:
        first_date = datetime.strptime(begin_date, '%d.%m.%Y')
        if end_date:
            second_date = datetime.strptime(end_date, '%d.%m.%Y')
            if pk == 0 or pk is None:
                events = Event.objects.filter(is_active=is_active,
                                              dates__date__range=(first_date, second_date + timedelta(1))).order_by('price')
            else:
                events = Event.objects.filter(is_active=is_active, category__pk=pk,
                                              dates__date__range=(first_date, second_date + timedelta(1))).order_by('price')
        else:
            if pk == 0 or pk is None:
                events = Event.objects.filter(is_active=is_active, dates__date=first_date).order_by('price')
            else:
                events = Event.objects.filter(is_active=is_active, category__pk=pk, dates__date=first_date).order_by('price')
    else:
        if pk == 0 or pk is None:
            events = Event.objects.all().order_by('price')
        else:
            events = Event.objects.filter(category__pk=pk).order_by('price')
    return events


def promo_events():
    return Event.objects.filter(is_promo=True, is_active=True)[:5]