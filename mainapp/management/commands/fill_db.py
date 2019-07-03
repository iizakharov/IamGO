import json
import os
import time

import requests
import tempfile

from django.core import files
from django.core.management.base import BaseCommand
from mainapp.models import EventCategory, EventAgent, EventLocation, Event, EventDate, EventGallery
from authapp.models import User

JSON_PATH = 'mainapp/json'

headers = {
    "Host": "afisha.yandex.ru",
    "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    'Cookie': 'yandexuid=8953047361557745751; i=TeW7KHmTTXDHc/IK27qr82slIxctisPJphlfm+/cHPfquMeg8djvt0DJhCig1G3+QryGKK'
              'kXfSZWFl8jwNKCgA1PpTc=; fuid01=5cd950593ec24d5a.rjvCB4G_QlaL4H_pnZ-s_nQH7X5pU-a1x64HBf2DUqItGK5R-pIDtDc'
              'OhdGN_D6NPiJ6rctFTHhYEAd8HmRtokT6eAhqgQ3UN50MuYfH2xdq4dIdVRfAesg1NBcZaN9T; _ym_uid=1557745754438948091; '
              'mda=0; yp=1574990764.szm.1:1920x1080:1920x924#1561875279.ygu.1; my=YwA=; bltsr=1; afisha.sid=s%3A_BGOD5Z'
              'wk9cVviTDNAMGi5gmdmtt5QgT.s3JSccAJyqfsaUFfgBSm1LHSk89D3p7bIxyBDbSA3t0; _ym_d=1560772064; specific=1; _cs'
              'rf=4GNHJF55ZDRKQ6p6vKaxWaVl; device_id="be5bcd72413e8c264213e909aaef7d63eeb1fd6e4"; rheftjdd=rheftjddVal'
              '; ys=wprid.1561727583382782-1701657974762114286500035-man1-3604',
    "Upgrade-Insecure-Requests": "1"
}


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        return json.load(infile)


def get_image_from_url(image_url):
    # Steam the image from the url
    request = requests.get(image_url, stream=True, headers=headers)

    # Was the request OK?
    if request.status_code != requests.codes.ok:
        # Nope, error handling, skip file etc etc etc
        return False

    # Get the filename from the url, used for saving later
    # file_name = image_url.split('/')[-1]

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)
    # image = Image()

    # Save the temporary image to the model#
    # This saves the model so be sure that is it valid
    # image.image.save(file_name, files.File(lf))
    # return image
    return {"image": files.File(lf)}


def create_categories():
    # Create categories
    categories = load_from_json('categories')
    print("Categories loaded")
    EventCategory.objects.all().delete()
    category_list = dict()
    for category in categories:
        category_list[category['name']] = category['description']
    [EventCategory.objects.create(name=key, description=value) for key, value in category_list.items()]
    print("Categories created")


def create_agents():
    # Create agents
    agents = load_from_json('agents')
    print("agents loaded")
    EventAgent.objects.all().delete()
    agent_list = dict()
    for agent in agents:
        agent_list[agent['name']] = agent['description']
    [EventAgent.objects.create(name=key, description=value) for key, value in agent_list.items()]
    print("Agents created")


def create_locations():
    # Create locations
    locations = load_from_json('locations')
    print("Locations loaded")
    EventLocation.objects.all().delete()
    location_list = dict()
    for location in locations:
        location_list[location['name']] = location['location']
    [EventLocation.objects.create(name=key, location=value) for key, value in location_list.items()]
    print("Locations created")


def create_events():
    # Create events
    locations = load_from_json('locations')
    categories = load_from_json('categories')
    events = load_from_json('events')
    print("Events loaded")
    Event.objects.all().delete()
    for event in events:
        # Create event
        event['agent'] = EventAgent.objects.get(name=event['agent'])
        event_object = Event.objects.create(**event)
        # print('{0} created.'.format(event['name']))
        # Add locations to event
        for location in locations:
            if event['name'] == location['event']:
                event_object.location.add(EventLocation.objects.get(name=location['name']))
        # Add categories to event
        for category in categories:
            if event['name'] == category['event']:
                event_object.category.add(EventCategory.objects.get(name=category['name']))

        # print('{0} is done.'.format(event['name']))
    print("Events created")


def create_dates():
    dates = load_from_json("eventdate")
    print("Dates loaded")
    EventDate.objects.all().delete()
    for i in dates:
        EventDate.objects.create(event=Event.objects.get(name=i["event"]), date=i["date"])
    print("Dates created")


def create_gallery():
    images = load_from_json("eventgallery")
    print("Gallery loaded")
    for idx, i in enumerate(images):
        print(f"Try get {idx}: ", end='')
        data = get_image_from_url(i['image'])
        if data:
            event_image = EventGallery.objects.create(event=Event.objects.get(name=i["event"]))
            event_image.image.save(i["event"] + f'{idx}', data['image'])
            time.sleep(1)
            print("Done")
        else:
            print("Fail")
    print("EventGallery done")


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_categories()
        create_agents()
        create_locations()
        create_events()
        create_dates()
        create_gallery()

        print("Recreate users: ", end='')
        User.objects.all().delete()
        User.objects.create_superuser('django@geekshop.local', 'geekbrains')
        User.objects.create_superuser("admin@admin.com", "password")
        print("Done")
