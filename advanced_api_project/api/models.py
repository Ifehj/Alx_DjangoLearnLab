from django.db import models

# Create your models here.

class Author(models.Model):
	name = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.name

class Book(models.Model):
	title = models.CharField(max_length=100, null=True)
	publication_year = models.IntegerField(null=True)
	author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.title} ({self.publication_year})"