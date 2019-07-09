from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login_view, name='login'),
    path('logout/', authapp.logout_view, name='logout'),
    path('register/', authapp.register_view, name='register'),
    path('edit/', authapp.edit_view, name='edit'),
]
