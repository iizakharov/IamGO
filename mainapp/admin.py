from django.contrib import admin
from mainapp.models import Event, EventCategory, EventAgent, EventLocation, EventDate, EventGallery


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    search_fields = 'name',


@admin.register(EventAgent)
class EventAgentAdmin(admin.ModelAdmin):
    search_fields = 'name',


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    search_fields = 'name',


@admin.register(EventDate)
class EventDateAdmin(admin.ModelAdmin):
    search_fields = 'date',


class EventGalleryInline(admin.TabularInline):
    model = EventGallery
    extra = 3


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = EventGalleryInline,
    search_fields = 'name', 'category__name',
    list_display = 'name',


@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    search_fields = 'event',
    list_display = 'event', 'image',
