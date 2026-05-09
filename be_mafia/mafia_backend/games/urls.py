from django.urls import path
from .views import GameListCreareView, GameDetailListView

urlpatterns = [
    path('games/', GameListCreareView.as_view()),
    path('games/<int:pk>/', GameDetailListView.as_view()),
]