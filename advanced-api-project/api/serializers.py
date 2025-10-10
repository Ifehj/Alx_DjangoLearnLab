from rest_framework import serializers
from .models import Book, Author
import datetime

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = "__all__"
	
	def validate_year_published(self, value):
		current_year = datetime.datetime.now().year
		if value > current_year:
			raise serializers.ValidationError("Publication year cannot be in the future.")
		return value

class AuthorSerializer(serializers.ModelSerializer):
	Books = BookSerializer(many=True, read_only=True)

	class Meta:
		model = Author
		fields = ['id', 'name', 'Books']

	