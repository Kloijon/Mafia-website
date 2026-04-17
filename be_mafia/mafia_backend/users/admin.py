from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
 list_display = ['id', 'nickname', 'slug', 'avatar', 'email', 'tg_username', 'elo', 'role']
 list_display_links =['id']
 list_filter = ['elo', 'role']
 list_editable =['nickname', 'avatar', 'email', 'tg_username', 'elo', 'role']
 search_fields = ['username', 'nickname']
 prepopulated_fields = {'slug': ('nickname',)}
