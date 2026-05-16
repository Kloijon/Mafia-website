from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
  list_display = ['id', 'username', 'avatar', 'email', 'tg_username', 'elo', 'is_staff',]
  list_editable = ['username', 'email', 'is_staff',]
  list_filter = ['elo', 'is_staff',]
  search_fields = ['username', 'email',]
  ordering = ['id']

  fieldsets = (
        (
            'Основное',
            {
                'fields': (
                    'username',
                    'password',
                    'email',
                    'avatar',
                    'tg_username',
                    'elo',
                )
            }
        ),

        (
            'Права',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                )
            }
        ),
    )

  add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),

                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                ),
            },
        ),
    )
