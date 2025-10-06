from django.db import models

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=100, null=True)
	author = models.CharField(max_length=100, null=True)