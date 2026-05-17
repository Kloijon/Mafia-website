from django.urls import path
from .views import UserListView, UserDetailView, RegisterView, MeView, UpdateProfileView

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/register/', RegisterView.as_view()),
    path('users/me/', MeView.as_view()),
    path('users/me/update/', UpdateProfileView.as_view()),
]