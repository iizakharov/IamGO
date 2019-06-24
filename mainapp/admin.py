from django.contrib import admin
from mainapp.models import Event, EventCategory, EventAgent, EventLocation, EventDate, EventGallery


class ProductInline(admin.TabularInline):
    model = Event
    fields = 'name', 'description'
    extra = 1


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    inlines = ProductInline,


@admin.register(EventAgent)
class EventAgentAdmin(admin.ModelAdmin):
    search_fields = 'name',


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    search_fields = 'name',


@admin.register(EventDate)
class EventDateAdmin(admin.ModelAdmin):
    search_fields = 'date',


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = 'name', 'category__name',
    list_display = 'name', 'category',


@admin.register(EventGallery)
class EventGalleryAdmin(admin.ModelAdmin):
    search_fields = 'event',
