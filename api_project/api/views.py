from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework import permissions
# Create your views here.

class BookList(generics.ListAPIView):
	permission_classes = [permissions.AllowAny]
	queryset = Book.objects.all()
	serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]

	queryset = Book.objects.all()
	serializer_class = BookSerializer