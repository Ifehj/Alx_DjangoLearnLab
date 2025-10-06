from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from django.urls import include
from .views import BookList

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),

    path('', include(router.urls)), 
]



