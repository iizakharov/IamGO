from django.core.management.base import BaseCommand
from mainapp.models import EventCategory, EventAgent, EventLocation, Event

import json
import os

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        EventCategory.objects.all().delete()
        [EventCategory.objects.create(**category) for category in categories]

        agents = load_from_json('agents')
        EventAgent.objects.all().delete()
        [EventAgent.objects.create(**agent) for agent in agents]

        locations = load_from_json('locations')

        EventLocation.objects.all().delete()
        [EventLocation.objects.create(**location) for location in locations]

        events = load_from_json('events')
        Event.objects.all().delete()

        for event in events:
            category_name = event['category']
            # Получаем категорию по имени
            _category = EventCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            event['category'] = _category
            Event.objects.create(**event)
