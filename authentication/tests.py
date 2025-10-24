from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestAuthViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='johndoe', password='12345')

    def test_login(self):
        response = self.client.post(reverse('authentication:login'), {
            'username': 'johndoe',
            'password': '12345'
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.login(username='johndoe', password='12345')
        response = self.client.get(reverse('authentication:logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
