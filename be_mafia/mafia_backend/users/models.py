from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
 first_name = None 
 last_name = None

 avatar = models.ImageField(upload_to='media/users_avatars/', null=True, blank=True)
 email = models.EmailField(unique=True, max_length=250)
 tg_username = models.CharField(max_length=100, unique=True, null=True, blank=True)
 elo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

 def __str__(self):
  return self.username