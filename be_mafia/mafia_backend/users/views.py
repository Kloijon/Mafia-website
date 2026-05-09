from rest_framework import generics
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer

# Create your views here.
class UserListView(generics.ListAPIView):
  queryset=User.objects.all().order_by('-elo')
  serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
  queryset=User.objects.all()
  serializer_class=UserSerializer

class RegisterView(generics.CreateAPIView):
  serializer_class=UserRegisterSerializer