from rest_framework import generics
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Prefetch
from .models import Game, UserPlay, Tournament
from .serializers import GameSerializer, GameCreateSerializer, TournamentSerializer

class IsAdminOrReadOnly(BasePermission):
  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    
    return request.user and request.user.is_staff

class TournamentListCreateView(generics.ListCreateAPIView):
  serializer_class = TournamentSerializer
  permission_classes = [IsAdminOrReadOnly]

  def get_queryset(self):
    queryset = Tournament.objects.all().order_by('-start_time')
    return queryset

class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Tournament.objects.all()
  serializer_class = TournamentSerializer
  permission_classes = [IsAdminOrReadOnly]
  
class GameListCreareView(generics.ListCreateAPIView):
  permission_classes = [IsAdminOrReadOnly]

  def get_queryset(self):
    return Game.objects.all().prefetch_related(Prefetch('players', 
                                                        queryset=UserPlay.objects.select_related('user').order_by('-id')))
  
  def get_serializer_class(self):
    if self.request.method == 'POST':
      return GameCreateSerializer
    return GameSerializer

class GameDetailListView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [IsAdminOrReadOnly]
  serializer_class = GameSerializer

  def get_queryset(self):
    return Game.objects.all().prefetch_related(Prefetch('players', 
                                               queryset=UserPlay.objects.select_related('user')))
  
class TournamentListCreateView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminOrReadOnly]