from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
	bio = models.CharField(max_length=100)
	profile_pictures = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
	followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

	def __str__(self):
		return self.username