from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def test_register_and_login(self):
        register_url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'ComplexPassw0rd!',
            'password2': 'ComplexPassw0rd!'
        }
        resp = self.client.post(register_url, data)
        self.assertEqual(resp.status_code, 302)
        login = self.client.login(username='testuser', password='ComplexPassw0rd!')
        self.assertTrue(login)
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)