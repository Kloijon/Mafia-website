from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
 ROLES = [
  ("player", "Player"),
  ("admin", "Admin"),
 ] 
 
 nickname = models.CharField(max_length=100, unique=True)
 slug = models.SlugField(max_length=100, unique=True)
 avatar = models.ImageField(upload_to='users_avatars/', null=True, blank=True)
 email = models.EmailField(unique=True)
 tg_username = models.CharField(max_length=100, unique=True, null=True, blank=True)
 elo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
 role = models.CharField(max_length=20, choices=ROLES, default="player")

 def __str__(self):
  return self.username
 

 

