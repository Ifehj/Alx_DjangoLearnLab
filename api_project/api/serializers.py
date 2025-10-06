from rest_framework import serializers
from .models import SimpleModel

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = SimpleModel
		fields = ['title', 'author']