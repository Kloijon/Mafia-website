from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
 list_display = ['id', 'title', 'post_type', 'published_at']
 list_filter = ['post_type', 'published_at']
 list_editable = ['title', 'post_type', 'published_at']
 search_fields = ['title']
 prepopulated_fields = {'slug': ('title',)}