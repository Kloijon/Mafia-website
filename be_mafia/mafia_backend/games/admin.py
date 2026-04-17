from django.contrib import admin
from .models import Game, Tournament, UserPlay

# Register your models here.
class UserPlayInline(admin.TabularInline):
    model = UserPlay
    extra = 1
    max_num = 10
    autocomplete_fields = ['user']

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
 list_display = ['id', 'referee', 'tournament', 'result']
 list_filter = ['referee', 'tournament', 'result']
 list_editable = ['referee', 'result']
 search_fields = ['referee']
 inlines = [UserPlayInline]

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
 list_display = ['id','title','start_time', 'place']
 list_filter = ['place']
 list_editable = ['title', 'start_time', 'place']
 search_fields = ['title']

@admin.register(UserPlay)
class UserPlayAdmin(admin.ModelAdmin):
 list_display = ['id', 'user', 'game', 'foul', 'tech_foul', 'play_role', 'score_plus', 'score_minus', 'score_ci', 'thoughts', 'protocol']
 list_filter = ['user', 'game', 'foul', 'tech_foul', 'play_role']
 list_editable = ['foul', 'tech_foul', 'score_plus', 'score_minus', 'score_ci']
 search_fields = ['user__username']
 