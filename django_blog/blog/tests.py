from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Post

class AuthenticationTests(TestCase):
    def test_register_and_login(self):
        # Register user
        resp = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Log out
        self.client.get(reverse('logout'))

        # Log in using test client (recommended way)
        login_successful = self.client.login(username='testuser', password='StrongPass123')
        self.assertTrue(login_successful)

class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass12345')
        self.other = User.objects.create_user(username='other', password='pass12345')
        self.post = Post.objects.create(title='Test', content='Content', author=self.user)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('post-create'))
        self.assertEqual(resp.status_code, 302)  # redirect to login

        self.client.login(username='author', password='pass12345')
        resp = self.client.get(reverse('post-create'))
        self.assertEqual(resp.status_code, 200)

    def test_only_author_can_edit(self):
        self.client.login(username='other', password='pass12345')
        resp = self.client.get(reverse('post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 403)  # UserPassesTestMixin returns 403 by default

        self.client.login(username='author', password='pass12345')
        resp = self.client.get(reverse('post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 200)