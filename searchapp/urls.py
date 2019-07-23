from django.urls import path

import searchapp.views as searchapp

app_name = 'searchapp'

urlpatterns = [
    path('view/', searchapp.SearchView.as_view(), name='view'),
]
