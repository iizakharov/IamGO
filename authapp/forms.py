import hashlib
import random
from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField
from authapp.models import User, UserProfile, UserActivation, UserSending


class UserAdminCreationForm(forms.ModelForm):
    # Форма для создания новых пользователей. Включает в себя все необходимые поля плюс повторный пароль.
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Проверка, что две записи пароля совпадают.
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        # Сохранение пароля в хешированном формате.
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """
    Форма для обновления пользователей.
    Включает в себя все поля пользователя, но заменяет поле редактирования пароля на поле чтения.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'staff', 'admin')

    def clean_password(self):
        return self.initial["password"]


class UserRegisterForm(forms.ModelForm):
    # Форма для регистрации.
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'is_sending')

    def clean_password2(self):
        # Проверка, что две записи пароля совпадают.
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_sending':
                self.fields[field_name].label = ''
                self.fields[field_name].widget.attrs.update({'class': 'registration-form-input'})

        self.fields['email'].widget.attrs.update(
            {
                'type': 'text',
                'placeholder': 'Email'
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'type': 'password',
                'placeholder': 'Придумайте пароль'
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'type': 'password',
                'placeholder': 'Повторите пароль'
            }
        )
        self.fields['is_sending'].widget.attrs.update(
            {
                'type': 'checkbox',
                'class': 'sending_checkbox'
            }
        )

    def save(self, commit=True):
        # Сохранение пароля в хешированном формате.
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        # Авторизация через email
        user.active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user_activation = UserActivation()
        user_activation.user = user
        user_activation.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user_activation.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'edit-form-input'
            field.help_text = ''


class UserProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(label=('Фото'), required=False, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('age', 'gender', 'avatar',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'edit-form-input'
        self.fields['avatar'].widget.attrs['class'] = 'edit-form-file'


class UserLoginForm(AuthenticationForm):
    # Форма для авторизации.
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name].label = ''

        self.fields['username'].widget.attrs.update(
            {
                'type': 'text',
                'class': 'registration-form-input',
                'placeholder': 'Email'
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'type': 'password',
                'class': 'registration-form-input',
                'placeholder': 'Пароль'
            }
        )


class UserSendingForm(forms.ModelForm):
    # Форма для рассылки.

    class Meta:
        model = UserSending
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'edit-form-input'
            self.fields[field_name].label = ''
            field.help_text = ''

        self.fields['email'].widget.attrs.update(
            {
                'type': 'text',
                'placeholder': 'Email'
            }
        )

