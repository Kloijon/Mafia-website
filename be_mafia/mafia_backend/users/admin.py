from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
 list_display = ['id', 'username', 'slug', 'avatar', 'email', 'tg_username', 'elo', 'is_staff']
 list_display_links =['id']
 list_filter = ['elo', 'is_staff']
 list_editable =['username', 'avatar', 'email', 'tg_username', 'elo', 'is_staff']
 search_fields = ['username', 'is_staff']
 prepopulated_fields = {'slug': ('username',)}
