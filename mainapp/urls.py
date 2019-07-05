from django.urls import path
# from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'


urlpatterns = [
    path('', mainapp.main, name='index'),
    path('', mainapp.main, name='events'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    path('events/', mainapp.events, name='events'),
]
