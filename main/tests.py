from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from io import BytesIO
from PIL import Image

from main.models import Iklan
from main.forms import IklanForm
from authentication.models import UserProfile


class MainViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.penyedia = User.objects.create_user(username='penyedia', password='testpass123')
        UserProfile.objects.create(user=self.user, role='user')
        UserProfile.objects.create(user=self.penyedia, role='penyedia')
    
    def _make_image_file(self, name="test.png"):
        buffer = BytesIO()
        image = Image.new("RGB", (1, 1), color=(255, 0, 0))
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type="image/png")
    
    def test_landing_page_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:landing_page'))
        self.assertEqual(response.status_code, 200)
    
    def test_landing_page_view_authenticated_penyedia(self):
        self.client.login(username='penyedia', password='testpass123')
        response = self.client.get(reverse('main:landing_page'))
        self.assertEqual(response.status_code, 200)
    
    def test_landing_page_view_unauthenticated(self):
        response = self.client.get(reverse('main:landing_page'))
        self.assertEqual(response.status_code, 200)
    
    def test_iklan_list_view(self):
        self.client.login(username='penyedia', password='testpass123')
        response = self.client.get(reverse('main:iklan_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_iklan_create_view_get(self):
        self.client.login(username='penyedia', password='testpass123')
        response = self.client.get(reverse('main:iklan_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], IklanForm)
    
    def test_iklan_create_view_post_valid(self):
        self.client.login(username='penyedia', password='testpass123')
        form_data = {
            'title': 'Test Iklan',
            'description': 'Test description',
            'price': 100000,
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        }
        image_file = self._make_image_file()
        response = self.client.post(reverse('main:iklan_create'), {**form_data, 'banner': image_file})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
    
    def test_iklan_create_view_post_invalid(self):
        self.client.login(username='penyedia', password='testpass123')
        form_data = {
            'title': '',
            'description': 'Test description',
            'price': 100000
        }
        response = self.client.post(reverse('main:iklan_create'), form_data)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
    
    def test_iklan_edit_view_get(self):
        self.client.login(username='penyedia', password='testpass123')
        iklan = Iklan.objects.create(
            title='Test Iklan',
            description='Test description',
            price=100000,
            host=self.penyedia
        )
        response = self.client.get(reverse('main:iklan_edit', args=[iklan.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_iklan_edit_view_post_valid(self):
        self.client.login(username='penyedia', password='testpass123')
        iklan = Iklan.objects.create(
            title='Test Iklan',
            description='Test description',
            price=100000,
            host=self.penyedia
        )
        form_data = {
            'title': 'Updated Iklan',
            'description': 'Updated description',
            'price': 150000
        }
        response = self.client.post(reverse('main:iklan_edit', args=[iklan.id]), form_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
    
    def test_iklan_delete_view_post(self):
        self.client.login(username='penyedia', password='testpass123')
        iklan = Iklan.objects.create(
            title='Test Iklan',
            description='Test description',
            price=100000,
            host=self.penyedia
        )
        response = self.client.post(reverse('main:iklan_delete', args=[iklan.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertFalse(Iklan.objects.filter(id=iklan.id).exists())
    
    def test_iklan_delete_view_get(self):
        self.client.login(username='penyedia', password='testpass123')
        iklan = Iklan.objects.create(
            title='Test Iklan',
            description='Test description',
            price=100000,
            host=self.penyedia
        )
        response = self.client.get(reverse('main:iklan_delete', args=[iklan.id]))
        self.assertEqual(response.status_code, 400)
    
    def test_news_list_view(self):
        response = self.client.get(reverse('main:news_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_news_create_view(self):
        response = self.client.get(reverse('main:news_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_wishlist_list_view(self):
        response = self.client.get(reverse('main:wishlist_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_wishlist_create_view(self):
        response = self.client.get(reverse('main:wishlist_create'))
        self.assertEqual(response.status_code, 200)