from django.shortcuts import render
from .models import EventCategory, Event


def get_main_menu():
    return EventCategory.objects.filter(is_active=True)


def get_event_by_date():
    return Event.objects.filter(category__is_active=True, is_active=True).order_by('date').select_related('category')


def main(request):
    title = 'Главная'
    main_menu = get_main_menu()
    event_by_date = get_event_by_date()[:3]
    context = {
        'title': title,
        "main_menu": main_menu,
        'event_by_date': event_by_date,
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
