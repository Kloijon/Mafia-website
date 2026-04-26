from rest_framework import generics, status
from rest_framework.permissions import BasePermissions, SAFE_METHODS
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Post
from .serializers import PostSerializer

class IsAdminOrReadOnly(BasePermissions):
  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    
    return request.user and request.user.is_staff

@method_decorator(cache_page(60 * 5), name='dispatch')
class PostListCreateView(generics.ListCreateAPIView):
  serializer_class = PostSerializer
  permission_classes = [IsAdminOrReadOnly]

  def get_queryset(self):
    queryset = Post.objects.all().order_by('-created_at')
    post_type = self.request.query_params.get('type')

    if post_type:
      queryset = queryset.filter(post_type=post_type)
    
    return queryset.filter(published_at__isnull=False)
  
  def perform_create(self, serializer):
    serializer.save()

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  permission_classes = [IsAdminOrReadOnly]