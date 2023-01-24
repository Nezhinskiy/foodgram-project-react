from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Администрирование пользователей.
    """
    list_display = ('username', 'id', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email', 'first_name')


@admin.register(Follow)
class SubscribeAdmin(admin.ModelAdmin):
    """
    Администрирование подписок на авторов.
    """
    list_display = ('user', 'author')
