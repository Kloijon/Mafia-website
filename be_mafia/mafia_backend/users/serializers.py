from rest_framework import serializers
from .models import User
from PIL import Image

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      'id',
      'username',
      'slug',
      'avatar',
      'email',
      'tg_username',
      'elo',
    ]
    read_only_fields = ['id', 'elo']
  
  def validate_username(self, value):
    if len(value) <= 2:
      raise serializers.ValidationError("Username должен состоять минимум из 3 символов")
    return value
  
  def validate_avatar(self, value):
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
  
  def validate_tg_username(self, value):
    if value and not value.startswith('@'):
      raise serializers.ValidationError("Tg username должен начинаться с @")
    return value
  
class UserRegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = [
      'username',
      'email',
      'password',
    ]

  def create(self, validated_data):
    user = User.objects.create_user(
      username = validated_data['username'],
      email = validated_data['email'],
      password = validated_data['password']
    )
    return user