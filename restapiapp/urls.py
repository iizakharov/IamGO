from django.urls import path
from django.conf.urls import url, include
from restapiapp.api import EventResource
from rest_framework import routers

from restapiapp.views import UserList

event_resource = EventResource()
app_name = 'restapiapp'

#router = routers.DefaultRouter()
#router.register(r'main', MainViewSet.as_view(), base_name='test')
print(event_resource.urls)
urlpatterns = [
    path('', UserList.as_view()),
    path('api/', include(event_resource.urls)),
]

