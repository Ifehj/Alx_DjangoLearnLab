from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import BookSerializer
from rest_framework import generics
from .models import Book
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class ListView(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [AllowAny]

	filter_backends = [DjangoFilterBackend, filters.SearchFilter]

	filterset_fields = ['title', 'author', 'publication_year']
	search_fields = ['title', 'author']

	ordering_fields = ['title', 'author', 'publication_year']
	ordering = ['title']  # default ordering

class DetailView(generics.RetrieveAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [AllowAny]
	
	

class CreateView(generics.CreateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]

class UpdateView(generics.UpdateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]
class DeleteView(generics.DestroyAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]