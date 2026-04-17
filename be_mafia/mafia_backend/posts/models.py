from django.db import models

# Create your models here.

class Post(models.Model):
  POST_TYPES = [
        ("news", "Новость"),
        ("announcement", "Анонс"),
    ]
  title = models.CharField(max_length=200)
  slug = models.SlugField(unique=True)
  content = models.TextField(null=True, blank=True)
  image = models.ImageField(upload_to='posts_images/', null=True, blank=True)
  tournament = models.ForeignKey(
        "games.Tournament",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
  )
  post_type = models.CharField(max_length=20, choices=POST_TYPES)
  created_at = models.DateTimeField(auto_now_add=True)
  published_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return self.title