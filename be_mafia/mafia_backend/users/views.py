from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer

# Create your views here.
class UserListView(generics.ListAPIView):
  queryset=User.objects.all().order_by('-elo')
  serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
  queryset=User.objects.all()
  serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
  serializer_class = UserRegisterSerializer

class MeView(generics.RetrieveAPIView):
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return self.request.user
  
class UpdateProfileView(generics.UpdateAPIView):
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return self.request.user
