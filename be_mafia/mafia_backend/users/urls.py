from django.urls import path
from .views import UserListView, UserDetailView, RegisterView, MeView, UpdateProfileView

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view()),
    path('me/update/', UpdateProfileView.as_view()),
]