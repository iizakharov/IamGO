from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse


def register_view(request):

    my_context = {
        'title': 'Регистрация',
    }

    return render(request, 'authapp/register.html', my_context)


def login_view(request):

    my_context = {
        'title': 'Авторизация',
    }

    return render(request, 'authapp/login.html', my_context)


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))
