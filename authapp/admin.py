from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from authapp.forms import UserAdminCreationForm, UserAdminChangeForm
from authapp.models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = UserProfileInline,

    # Формы для добавления / изменения пользователей в UserAdmin
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm

    # Поля, которые будут использоваться при отображении модели пользователя
    # Переопределяет поля в UserAdmin
    list_display = ('email', 'active', 'staff', 'admin',)
    list_filter = ('staff', 'active', 'admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Доступы', {'fields': ('active', 'staff', 'admin',)}),
    )

    # add_fieldsets не является стандартным атрибутом ModelAdmin. UserAdmin
    # Переопределяет get_fieldsets для создания пользвателя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'active', 'staff', 'admin',)}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Разработать Group Model для админки
admin.site.unregister(Group)
