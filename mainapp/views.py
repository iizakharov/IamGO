import datetime

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import EventCategory, Event, EventDate
from .utils import weekend_events, kid_events, free_events, health_events


def get_main_menu():
    return EventCategory.objects.filter(is_active=True).order_by('-name')


def get_event_by_date():
    return Event.objects.filter(is_active=True).order_by('date')


def get_event_today():
    return EventDate.objects.filter(date__contains=datetime.date.today())


def get_events_tomorrow():
    return EventDate.objects.filter(date__contains=datetime.date.today() + datetime.timedelta(days=1))


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
    if 'date' in request.GET.keys():
        date_filter = request.GET['date']
    else:
        date_filter = None
    print(f'Date filter: {date_filter}')
    if pk is not None:
        if pk == 0:
            events = Event.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(EventCategory, pk=pk)
            events = Event.objects.filter(category__pk=pk).order_by('price')
        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'events': events,
            'main_menu': main_menu,
        }
        return render(request, 'mainapp/events_list.html', content)
    events_all = get_events()
    today = get_event_today()
    tomorrow = get_events_tomorrow()
    content = {
        'title': title,
        'links_menu': links_menu,
        'events_all': events_all,
        'main_menu': main_menu,
        'today': today,
        'tomorrow': tomorrow,
    }

    return render(request, 'mainapp/events.html', content)
