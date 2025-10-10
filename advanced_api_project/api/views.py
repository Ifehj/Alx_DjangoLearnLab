from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
# Create your views here.

class ListView(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]

	filter_backends = [filter.SearchFilter]
	search_fields = ['title', 'author_name']

class DetailView(generics.RetrieveAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]

class CreateView(generics.CreateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

class UpdateView(generics.UpdateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]
class DeleteView(generics.DestroyAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]