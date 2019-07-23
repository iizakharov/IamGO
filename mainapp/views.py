from datetime import datetime, timedelta, date

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import EventCategory, Event, EventDate
from .utils import weekend_events, kid_events, free_events, health_events, get_filter_events, get_weekends_dates


def get_main_menu():
    return EventCategory.objects.filter(is_active=True).order_by('-name')


def get_event_by_date():
    return Event.objects.filter(is_active=True).order_by('date')


def get_event_today():
    return EventDate.objects.filter(date__contains=date.today())


def get_events_tomorrow():
    return EventDate.objects.filter(date__contains=date.today() + timedelta(days=1))


def get_expect_concert():
    # return Event.objects.filter(category__name='Концерты').filter(is_hot=True)
    return Event.objects.filter(category__name='Концерт')


def get_collections():
    return {
        "Куда сходить в выходные": weekend_events(),
        "Куда сходить с детьми": kid_events(),
        "Бесплатно": free_events(),
        "Здоровый образ жизни": health_events()
    }


def get_events():
    return Event.objects.filter(is_active=True)


def get_events_first_filter():
    return Event.objects.all().order_by("price")[5:8]


def main(request):
    title = 'Главная'
    main_menu = get_main_menu()[:8]
    event_by_date = get_event_by_date()[:3]
    first_filter = get_events_first_filter()
    expect_concert = get_expect_concert()[1:4]
    collections = get_collections()
    today = get_event_today()
    tomorrow = get_events_tomorrow()
    context = {
        'title': title,
        "main_menu": main_menu,
        'event_by_date': event_by_date,
        'expect_concert': expect_concert,
        'collections': collections,
        'first_filter': first_filter,
        'today': today,
        'tomorrow': tomorrow,
    }
    return render(request, 'mainapp/index.html', context)


def product(request, pk=None):
    main_menu = get_main_menu()[:8]
    event = get_object_or_404(Event, pk=pk)
    related_events = Event.objects.filter(is_active=True).filter(~Q(pk=pk)).order_by("?")[:3]

    content = {
        'title': 'Мероприятие',
        'event': event,
        'avatar': event.get_avatar,
        'related_events': related_events,
        'main_menu': main_menu,
    }

    return render(request, 'mainapp/product.html', content)


def collections_view(request, pk):
    collections = get_collections()
    if pk >= len(collections):
        pk = 0
    title = 'Мероприятия'
    category = dict()
    category['name'] = list(collections.keys())[pk]
    events = list(collections.values())[pk]
    links_menu = EventCategory.objects.all()
    main_menu = get_main_menu()[:8]
    content = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'events': events,
        'main_menu': main_menu,
        # 'events_by_date': events_by_date,
    }
    return render(request, 'mainapp/events_list.html', content)


def events(request, pk=None):
    title = 'мероприятия'
    links_menu = EventCategory.objects.all()
    main_menu = get_main_menu()[:8]
    # Check date filter
    if 'first_date' in request.GET.keys():
        first_date = request.GET['first_date']
    else:
        first_date = None
    if 'second_date' in request.GET.keys():
        second_date = request.GET['second_date']
    else:
        second_date = None
    print(f'Date filter: {first_date} -- {second_date}')
    category = {'name': 'Все события'}
    if pk is not None:
        if pk != 0:
            category = get_object_or_404(EventCategory, pk=pk)
    current_events = get_filter_events(pk=pk, begin_date=first_date, end_date=second_date)
    weekend = get_weekends_dates()
    content = {
        'title': title,
        'links_menu': links_menu,
        'category': category,
        'events': current_events,
        'main_menu': main_menu,
        'today': date.today().strftime('%d.%m.%Y'),
        'tomorrow': (date.today() + timedelta(1)).strftime('%d.%m.%Y'),
        'first_date': weekend['first_date'],
        'second_date': weekend['last_date']
    }
    return render(request, 'mainapp/events_list.html', content)
