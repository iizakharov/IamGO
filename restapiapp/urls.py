from django.urls import path, reverse
from django.conf.urls import url, include
from rest_framework import routers
from restapiapp.views import EventViewSet, EventCategoryViewSet, EventGalleryViewSet
from restapiapp.views import EventDateViewSet, EventLocationViewSet, EventAgentViewSet

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'categories', EventCategoryViewSet)
router.register(r'galleries', EventGalleryViewSet)
router.register(r'dates', EventDateViewSet)
router.register(r'locations', EventLocationViewSet)
router.register(r'agents', EventAgentViewSet)

app_name = 'restapiapp'

#router = routers.DefaultRouter()
#router.register(r'main', MainViewSet.as_view(), base_name='test')

urlpatterns = [
    # path('', UserList.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('events/', include(event_resource.urls))
]
