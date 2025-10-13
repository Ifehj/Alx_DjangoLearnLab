from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

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
