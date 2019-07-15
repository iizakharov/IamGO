import json
import os
import shutil
from collections import defaultdict

import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from mainapp.models import EventCategory, EventAgent, EventLocation, Event, EventDate, EventGallery
from authapp.models import User

JSON_PATH = 'mainapp/json'
base_url = 'http://127.0.0.1:8000/api/v1/'
username = 'admin@admin.com'
password = 'password'
_id_cache = defaultdict(dict)


def get_url(name):
    return base_url + name + '/'


def get_category_id(name):
    return get_id('categories', name)


def get_agent_id(name):
    return get_id('agents', name)


def get_location_id(name):
    return get_id('locations', name)


def get_event_id(name):
    return get_id('events', name)


def get_id(model, name):
    if _id_cache[model].get(name):
        return _id_cache[model].get(name)
    else:
        payload = {'name': name}
        request = requests.get(get_url(model), params=payload)
        if request.status_code == 200:
            if len(request.json()) > 0:
                _id_cache[model][request.json()[0]['name']] = request.json()[0]['id']
                return request.json()[0]['id']
            else:
                return None
        return None


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


def create_categories():
    # Create categories
    url = get_url('categories')
    categories = load_from_json('categories')
    print("Categories loaded")
    unique_categories = dict()
    for category in categories:
        category.pop('event')
        unique_categories[category['name']] = category
    EventCategory.objects.all().delete()
    for name, data in unique_categories.items():
        request = requests.post(url=url, auth=requests.auth.HTTPBasicAuth(username, password), json=data)
        if request.status_code == 201:
            print(f"{name} created")
        else:
            print(f"{name}: {request.status_code}\t{request.text}")
    print(10 * "=", "Categories created", 10 * "=")


def create_agents():
    # Create agents
    url = get_url('agents')
    agents = load_from_json('agents')
    print("agents loaded")
    EventAgent.objects.all().delete()
    for agent in agents:
        request = requests.post(url=url, auth=requests.auth.HTTPBasicAuth(username, password), json=agent)
        if request.status_code == 201:
            print(f"{agent['name']} created")
        else:
            print(f"{agent['name']}: {request.status_code}\t{request.text}")
    print(10 * "=", "Agents created", 10 * "=")


def create_locations():
    # Create locations
    url = get_url('locations')
    locations = load_from_json('locations')
    print("Locations loaded")
    EventLocation.objects.all().delete()
    unique_locations = dict()
    for location in locations:
        location.pop('event')
        unique_locations[location['name']] = location
    for name, data in unique_locations.items():
        request = requests.post(url=url, auth=requests.auth.HTTPBasicAuth(username, password), json=data)
        if request.status_code == 201:
            print(f"{name} created")
        else:
            print(f"{name}: {request.status_code}\t{request.text}")
    print(10 * "=", "Locations created", 10 * "=")


def create_events():
    # Create events
    url = get_url('events')
    events = load_from_json('events')
    print("Events loaded")
    Event.objects.all().delete()
    for event in events:
        # Create event
        event['agent'] = get_agent_id(event['agent'])
        request = requests.post(url=url, auth=requests.auth.HTTPBasicAuth(username, password), json=event)
        if request.status_code == 201:
            print(f"{event['name']} created")
        else:
            print(f"{event['name']}: {request.status_code}\t{request.text}")
        # print('{0} created.'.format(event['name']))
        # Add locations to event
        # for location in locations:
        #     if event['name'] == location['event']:
        #         event_object.location.add(EventLocation.objects.get(name=location['name']))
        # # Add categories to event
        # for category in categories:
        #     if event['name'] == category['event']:
        #         event_object.category.add(EventCategory.objects.get(name=category['name']))
        #
        # # print('{0} is done.'.format(event['name']))
    print(10 * "=", "Events created", 10 * "=")


def create_dates():
    # Create dates
    url = get_url('dates')
    dates = load_from_json("eventdate")
    print("Dates loaded")
    EventDate.objects.all().delete()
    for date in dates:
        date['event'] = get_event_id(date['event'])
        request = requests.post(url=url, auth=requests.auth.HTTPBasicAuth(username, password), json=date)
        if request.status_code == 201:
            print(f"{date['date']} created")
        else:
            print(f"{date['date']}: {request.status_code}\t{request.text}")
    print(10 * "=", "Dates created", 10 * "=")


def create_gallery():
    url = get_url('galleries')
    galleries = load_from_json('eventgallery')
    print("Galleries loaded")
    EventGallery.objects.all().delete()
    if os.path.exists(f"{settings.STATICFILES_DIRS[0]}/img/tmp/"):
        shutil.rmtree(f"{settings.STATICFILES_DIRS[0]}/img/tmp/")
    for image in galleries:
        image['event'] = get_event_id(image['event'])
        image['is_avatar'] = True if image['is_avatar'] == "true" else False
        # Create image
        request = requests.post(url=url, auth=requests.auth.HTTPBasicAuth(username, password), json=image)
        if request.status_code == 201:
            print(f"{image['image']:50} created... \t", end='')
            # Upload image
            file = {'image': (f"{image['image']}.png",
                              open(f"{settings.STATICFILES_DIRS[0]}/img/origin/{image['image']}", 'rb'))}
            upload = requests.put(url=f"{url}{request.json()['id']}/image/",
                                  auth=requests.auth.HTTPBasicAuth(username, password), files=file)
            if upload.status_code == 200:
                print(f"uploaded")
            else:
                print(f"fail upload: {request.status_code}\t{request.text}")
                file = {'image': (f"{image['image']}.png",
                                  open(f"{settings.STATICFILES_DIRS[0]}/img/s372x223_lelingrad.webp", 'rb'))}
                upload = requests.put(url=f"{url}{request.json()['id']}/image/",
                                      auth=requests.auth.HTTPBasicAuth(username, password), files=file)
                if upload.status_code == 200:
                    print(f"{image['image']:50} uploaded temp file")
                else:
                    print(f"{image['image']:50} fail upload temp file: {request.status_code}\t{request.text}")
        else:
            print(f"{image['image']}: {request.status_code}\t{request.text}")
    print(10 * "=", "Images created and uploaded", 10 * "=")


def update_locations_in_event():
    locations = load_from_json('locations')
    url = get_url('events')
    events_id = defaultdict(list)
    for location in locations:
        event_id = get_event_id(location['event'])
        location_id = get_location_id(location['name'])
        events_id[event_id].append(location_id)
    for key, value in events_id.items():
        data = list()
        for val in value:
            data.append(("location", (None, val)))
        request = requests.put(url=f"{url}{key}/location/", auth=requests.auth.HTTPBasicAuth(username, password),
                               files=data)
        if request.status_code == 200:
            print(f"{key} created")
        else:
            print(f"{key}: {request.status_code}\t{request.text}")
    print(10 * "=", "Links locations and events created", 10 * "=")


def update_categories_in_event():
    categories = load_from_json('categories')
    url = get_url('events')
    events_id = defaultdict(list)
    for category in categories:
        event_id = get_event_id(category['event'])
        category_id = get_category_id(category['name'])
        events_id[event_id].append(category_id)
    for key, value in events_id.items():
        data = list()
        for val in value:
            data.append(("category", (None, val)))
        request = requests.put(url=f"{url}{key}/category/", auth=requests.auth.HTTPBasicAuth(username, password),
                               files=data)
        if request.status_code == 200:
            print(f"{key} created")
        else:
            print(f"{key}: {request.status_code}\t{request.text}")
    print(10 * "=", "Links categories and events created", 10 * "=")


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        User.objects.create_superuser('django@geekshop.local', 'geekbrains')
        User.objects.create_superuser(username, password)
        create_categories()
        create_agents()
        create_locations()
        create_events()
        create_dates()
        create_gallery()
        update_locations_in_event()
        update_categories_in_event()
