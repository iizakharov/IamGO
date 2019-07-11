from django.urls import path
from django.conf.urls import url, include
from tastypie.api import Api
from restapiapp.api import EventResource, EventCategoryResource, EventAgentResource, EventLocationResource
from rest_framework import routers

from restapiapp.views import UserList

v1_api = Api(api_name='v1')
v1_api.register(EventResource())
v1_api.register(EventCategoryResource())
v1_api.register(EventAgentResource())
v1_api.register(EventLocationResource())
event_resource = EventResource()
app_name = 'restapiapp'

#router = routers.DefaultRouter()
#router.register(r'main', MainViewSet.as_view(), base_name='test')
print(event_resource.urls)
urlpatterns = [
    path('', UserList.as_view()),
    path('api/', include(v1_api.urls)),
]

