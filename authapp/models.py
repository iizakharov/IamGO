import os
from uuid import uuid4
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.deconstruct import deconstructible
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta


def get_activation_key_time():
    return now() + timedelta(hours=48)


# Менеджер модели пользователя
class UserManager(BaseUserManager):
    # Создает и сохраняет пользователя с указанным адресом электронной почты и паролем
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Адрес электронной почты - обязательный параметр')

        if not password:
            raise ValueError('Пароль - обязательный параметр')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    # Создает и сохраняет сотрудника с указанным адресом электронной почты и паролем
    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    # Создает и сохраняет суперпользователя с указанным адресом электронной почты и паролем
    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


@deconstructible
class PathAndRename(object):
    # Преобразует название загружаемого изображения
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{uuid4().hex}.{ext}'

        return os.path.join(self.path, filename)


path_and_rename = PathAndRename("static/img/tmp")


class User(AbstractBaseUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=255,
        unique=True,
    )

    active = models.BooleanField(default=True, verbose_name='Активный')
    staff = models.BooleanField(default=False, verbose_name='Сотрудник')  # a admin user; non super-user
    admin = models.BooleanField(default=False, verbose_name='Администратор')  # a superuser

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email и пароль обязательны к заполнению по умолчанию

    def get_full_name(self):
        # Пользователь идентифицируется по его адресу электронной почты
        return self.email

    def get_short_name(self):
        # Пользователь идентифицируется по его адресу электронной почты
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # У пользователя есть определенное разрешение? Самый простой ответ: да, всегда
        return True

    def has_module_perms(self, app_label):
        # Есть ли у пользователя права на просмотр приложения "app_label"? Самый простой ответ: да, всегда
        return True

    @property
    def is_staff(self):
        # Пользователь - сотрудник?
        return self.staff

    @property
    def is_admin(self):
        # Пользователь - администратор?
        return self.admin

    @property
    def is_active(self):
        # Пользователь - активный?
        return self.active


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(verbose_name='Возраст', null=True, blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    avatar = models.ImageField(
        upload_to=path_and_rename,
        default='static/img/default_user_avatar.png',
        verbose_name='Изображение пользователя',
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)  # create
        else:
            instance.userprofile.save()  # save form

    def __str__(self):
        return self.user.email


class UserActivation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_time)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
