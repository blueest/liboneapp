from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='default_profile.png')
    background_image = models.ImageField(upload_to='background_images/', default='default_background.jpg')
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(max_length=300, blank=True)
    job = models.CharField(max_length=100, blank=True)
    hobbies = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.user.username
