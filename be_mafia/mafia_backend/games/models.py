from django.db import models
from users.models import User

# Create your models here.

class Tournament(models.Model):
 title = models.CharField(max_length=100, unique=True)
 description = models.TextField(null=True, blank=True)
 image = models.ImageField(upload_to='tournaments_image/', null=True, blank=True)
 start_time = models.DateTimeField()
 place = models.CharField(max_length=150)
 
 def __str__(self):
  return self.title

class Game(models.Model):
 RESULT_CHOICES = [
  ("Red", "Красные"),
  ("Black", "Чёрные"),
  ]

 referee = models.CharField(max_length=100)
 tournament = models.ForeignKey("games.Tournament", on_delete=models.SET_NULL, null=True, blank=True)
 result = models.CharField(max_length=20, choices=RESULT_CHOICES, default="Red")

 def __str__(self):
  return self.id


class Role(models.TextChoices):
 MAFIA = "mafia", "Мафия" 
 DON = "don", "Дон" 
 SHERIFF = "sheriff", "Шериф" 
 CIVILIAN = "civilian", "Мирный"

 
class UserPlay(models.Model):
 FOUL_CHOICE = [
  (0, "0"),
  (1, "1"),
  (2, "2"),
  (3, "3"),
  (4, "4"),
 ]
 TECH_FOUL_CHOICE = [
  (0, "0"),
  (1, "1"),
  (2, "2"),
 ]
 
 user = models.ForeignKey('users.User', on_delete=models.CASCADE)
 game = models.ForeignKey("games.Game", on_delete=models.CASCADE)
 foul = models.IntegerField(default=0, choices=FOUL_CHOICE)
 tech_foul = models.IntegerField(default=0, choices=TECH_FOUL_CHOICE)
 play_role = models.CharField(max_length=20, choices=Role.choices)
 score_plus = models.DecimalField(null=True, max_digits=5, decimal_places=1)
 score_minus = models.DecimalField(null=True, max_digits=5, decimal_places=1)
 score_ci = models.DecimalField(null=True, max_digits=5, decimal_places=1)
 thoughts = models.TextField(null=True, blank=True)
 protocol = models.TextField(null=True, blank=True)

 class Meta:
  unique_together = ("user", "game")

 def __str__(self):
  return f"{self.user} in game {self.game_id}"
