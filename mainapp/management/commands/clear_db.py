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
        EventCategory.objects.all().delete()
        EventAgent.objects.all().delete()
        EventLocation.objects.all().delete()
        Event.objects.all().delete()
