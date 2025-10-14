from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)

	class Meta:
		ordering = ['name']
	
	def __str__(self):
		return self.name
	
class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	tags = TaggableManager()

	def __str__(self):
		return self.title

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	website = models.URLField(blank=True)
	location = models.CharField(max_length=30, blank=True)

	def __str__(self):
		return f'Profile({self.user.username})'
	
class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Comment by {self.author.username} on {self.Post.title}'

	class Meta:
		ordering = ['-created_at']
	
	def get_absolute_url(self):
		# on successful edit/delete we redirect to the post detail
		return reverse('post-detail', kwargs={'pk': self.post.pk})



