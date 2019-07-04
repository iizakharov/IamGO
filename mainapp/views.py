from django.shortcuts import render, get_object_or_404
from .models import EventCategory, Event, EventCollection


def get_main_menu():
    return EventCategory.objects.filter(is_active=True)


def get_event_by_date():
    return Event.objects.filter(is_active=True).order_by('date')


def get_expect_concert():
    return Event.objects.filter(category__name='Концерты').filter(is_hot=True)


def get_collections():
    return EventCollection.objects.filter(is_active=True)


def main(request):
    title = 'Главная'
    main_menu = get_main_menu()
    event_by_date = get_event_by_date()[:3]
    expect_concert = get_expect_concert()
    collections = get_collections()
    context = {
        'title': title,
        "main_menu": main_menu,
        'event_by_date': event_by_date,
        'expect_concert': expect_concert,
        'collections': collections,
    }
    return render(request, 'mainapp/index.html', context)


def product(request, pk=None):
    print(pk)
    # event = Event.objects.filter(pk=pk).prefetch_related().first()
    event = get_object_or_404(Event, pk=pk)
    print(event.dates.first().date)

    content = {
        'title': 'Мероприятие',
        'event': event
    }

    return render(request, 'mainapp/product.html', content)


def events(request):
    content = {
        'title': 'Все похожие мероприятия',
    }

    return render(request, 'mainapp/events.html', content)
