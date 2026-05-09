from django.urls import path
from .views import UserListView, UserDetailView, RegisterView

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('register/', RegisterView.as_view()),
]