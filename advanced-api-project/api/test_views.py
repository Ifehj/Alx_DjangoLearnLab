from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author



class BookAPITests(APITestCase):

    def setUp(self):
        """Initialize test data and authentication setup."""
        # Create a user for authenticated operations
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        # Create an author
        self.author = Author.objects.create(name="John Doe")

        # Create some books
        self.book1 = Book.objects.create(
            title="Django Basics",
            author=self.author,
            publication_year=2023
        )
        self.book2 = Book.objects.create(
            title="Advanced Django",
            author=self.author,
            publication_year=2022
        )

        # Setup API client
        self.client = APIClient()
        
        # Common endpoint URLs
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", args=[self.book1.id])
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", args=[self.book1.id])
        self.delete_url = reverse("book-delete", args=[self.book1.id])

    # ---------- CRUD TESTS ----------

    def test_list_books(self):
        """Test GET request to list all books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Advanced Django")

    def test_retrieve_book(self):
        """Test GET request to retrieve a single book."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Django Basics")

    def test_create_book_unauthenticated(self):
        """Test POST request without authentication (should fail)."""
        data = {"title": "New Book", "author": self.author.id, "publication_year": 2024}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Test POST request with authentication (should pass)."""
        self.client.login(username="testuser", password="testpassword")
        data = {"title": "New Book", "author": self.author.id, "publication_year": 2024}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_update_book_authenticated(self):
        """Test PUT request to update an existing book."""
        self.client.login(username="testuser", password="testpassword")
        data = {"title": "Django Updated", "author": self.author.id, "publication_year": 2023}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Django Updated")

    def test_delete_book_authenticated(self):
        """Test DELETE request for a book."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ---------- FILTER, SEARCH, ORDER TESTS ----------

    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication_year."""
        response = self.client.get(f"{self.list_url}?publication_year=2023")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Django Basics")

    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get(f"{self.list_url}?search=Advanced")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Advanced Django")

    def test_order_books_by_publication_year(self):
        """Test ordering books by publication_year."""
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["publication_year"], 2022)
