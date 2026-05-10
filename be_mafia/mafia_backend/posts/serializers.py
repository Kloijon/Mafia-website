# определяет сериализаторы для модели posts
from rest_framework import serializers
from .models import Post
from PIL import Image

class PostSerializer(serializers.ModelSerializer):
  # базовый сериализатор для модели post
  class Meta:
    model = Post
    fields = ['id', 'title', 'slug', 'content', 'image', 'post_type', 'created_at', 'published_at']
    read_only_fields = ['id', 'slug', 'created_at']

  def validate_title(self, value):
    if not value.strip():
      raise serializers.ValidationError('Заголовок не может быть пустым') 
    return value.strip()
  
  def validate_content(self, value):
    if not value.strip():
      raise serializers.ValidationError('Описание не может быть пустым') 
    return value.strip()
  
  def validate_image(self, value):
    if value:
      if value.size > 5 * 1024 * 1024:
        raise serializers.ValidationError('Максимальный размер файла - 5 МБ')
      try:
        img = Image.open(value)
        img.verify()
        value.seek(0)
      except Exception:
        raise serializers.ValidationError('Некорректное изображение')
    return value
