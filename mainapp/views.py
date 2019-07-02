from django.shortcuts import render
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


def product(request):
    content = {
        'title': 'Мероприятие',
    }

    return render(request, 'mainapp/product.html', content)


def events(request):
    content = {
        'title': 'Все похожие мероприятия',
    }

    return render(request, 'mainapp/events.html', content)
