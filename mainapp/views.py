from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import EventCategory, Event, EventCollection


def get_main_menu():
    return EventCategory.objects.filter(is_active=True).order_by('-name')


# не работает!
def get_event_by_date():
    return Event.objects.filter(is_active=True).order_by('date')


def get_expect_concert():
    # return Event.objects.filter(category__name='Концерты').filter(is_hot=True)
    return Event.objects.filter(category__name='Концерт')


def get_collections():
    return EventCollection.objects.filter(is_active=True)


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
    context = {
        'title': title,
        "main_menu": main_menu,
        'event_by_date': event_by_date,
        'expect_concert': expect_concert,
        'collections': collections,
        'first_filter': first_filter,
    }
    return render(request, 'mainapp/index.html', context)


def product(request, pk=None):
    print(pk)
    # event = Event.objects.filter(pk=pk).prefetch_related().first()
    main_menu = get_main_menu()[:8]
    event = get_object_or_404(Event, pk=pk)
    related_events = Event.objects.filter(is_active=True).filter(~Q(pk=pk)).order_by("?")[:3]
    print(related_events[0].images.first().image.url)
    try:
        avatar = '/' + event.images.filter(is_avatar=True).first().image.url
    except AttributeError:
        avatar = '/static/img/s372x223_lelingrad.webp'

    content = {
        'title': 'Мероприятие',
        'event': event,
        'avatar': avatar,
        'related_events': related_events,
        'main_menu': main_menu,
    }

    return render(request, 'mainapp/product.html', content)


def events(request, pk=None):
    print(pk)

    title = 'мероприятие'
    links_menu = EventCategory.objects.all()
    main_menu = get_main_menu()[:8]

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
    test_event = Event.objects.all()

    content = {
        'title': title,
        'links_menu': links_menu,
        'events_all': events_all,
        'main_menu': main_menu,
    }

    return render(request, 'mainapp/events.html', content)
