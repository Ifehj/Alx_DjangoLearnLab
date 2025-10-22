from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
<<<<<<< HEAD
	bio = models.TextField(max_length=100)
=======
	bio = models.CharField(max_length=100)
>>>>>>> 79dfd475dc9d4fec0bdc37ab5a5c0c17ccec2c9e
	profile_pictures = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
	followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

	def __str__(self):
		return self.username