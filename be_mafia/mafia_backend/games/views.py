from rest_framework import generics
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Prefetch
from .models import Game, UserPlay
from .serializers import GameSerializer, GameCreateSerializer

class IsAdminOrReadOnly(BasePermission):
  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    
    return request.user and request.user.is_staff
  
class GameListCreareView(generics.ListCreateAPIView):
  permission_classes = [IsAdminOrReadOnly]

  def get_queryset(self):
    return Game.objects.all().prefetch_related(Prefetch('userplay_set', 
                                                        queryset=UserPlay.objects.select_related('user').order_by('-id')))
  
  def get_serializer_class(self, request):
    if self.request.method == 'POST':
      return GameCreateSerializer
    return GameSerializer

class GameDetailListView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [IsAdminOrReadOnly]
  serializer_class = GameSerializer

  def get_queryset(self):
    return Game.objects.all().prefetch_related(Prefetch('userplay_set'), 
                                               queryset=UserPlay.objects.select_related('user'))
  
  