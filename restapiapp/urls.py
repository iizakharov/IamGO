from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from restapiapp.views import EventViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)

app_name = 'restapiapp'

#router = routers.DefaultRouter()
#router.register(r'main', MainViewSet.as_view(), base_name='test')

urlpatterns = [
    # path('', UserList.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('events/', include(event_resource.urls))
]

