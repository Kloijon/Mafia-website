from django.urls import path
from .views import GameListCreareView, GameDetailListView, TournamentListCreateView, TournamentDetailView

urlpatterns = [
    path('games/', GameListCreareView.as_view()),
    path('games/<int:pk>/', GameDetailListView.as_view()),
    path('tournaments/', TournamentListCreateView.as_view()),
    path('tournaments/<int:pk>/', TournamentDetailView.as_view()),
]