from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from authapp.forms import User, UserRegisterForm, UserLoginForm, UserProfileEditForm, UserEditForm, UserSendingForm


def register_view(request):
    title = 'Регистрация'

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save()
            if send_verify_mail(new_user):
                # print('confirmation message sent')
                return render(request, 'authapp/verification.html')
            else:
                # print('error sending message')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = UserRegisterForm()

    my_context = {
        'title': title,
        'register_form': register_form,
    }

    return render(request, 'authapp/register.html', my_context)


def login_view(request):
    title = 'Вход'

    login_form = UserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))

    my_context = {
        'title': title,
        'login_form': login_form,
        'next': next
    }

    return render(request, 'authapp/login.html', my_context)


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def edit_view(request):
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=request.user.userprofile)

        if edit_form.is_valid()and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('mainapp:index'))
    else:
        edit_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    my_context = {
        'title': 'Страница пользователя',
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/edit.html', my_context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', kwargs={'email': user.email, 'activation_key': user.useractivation.activation_key})
    title = f'Account Verification {user.email}'
    message = f'To confirm your account {user.email} on the portal ' \
        f'{settings.DOMAIN_NAME} follow the link: {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.useractivation.activation_key == activation_key and not user.useractivation.is_activation_key_expired():
            user.active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('auth:login'))


def sending_view(request):
    title = 'Подписка на рассылку'

    sending_form = UserSendingForm(data=request.POST or None)

    if request.method == 'POST' and sending_form.is_valid():
        sending_form.save()
        return render(request, 'authapp/verification.html')

    my_context = {
        'title': title,
        'sending_form': sending_form,
    }

    return render(request, 'authapp/sending.html', my_context)
