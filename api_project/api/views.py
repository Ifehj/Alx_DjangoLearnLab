from django.shortcuts import render
from rest_framework import generics
from .models import SimpleModel
from .serializer import BookSerializer
# Create your views here.

class BookList(generics.ListAPIView):
	queryset = SimpleModel.objects.all()
	serializer_class = BookSerializer
