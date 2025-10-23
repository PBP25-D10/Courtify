from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from io import BytesIO
from PIL import Image

from artikel.models import News
from artikel.forms import NewsForm
from authentication.models import UserProfile


class ArtikelViewsTest(TestCase):
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
    
    def test_news_list_view_penyedia(self):
        self.client.login(username='penyedia', password='testpass123')
        response = self.client.get(reverse('artikel:news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('news_list', response.context)
        self.assertIn('form', response.context)
    
    def test_news_list_view_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('artikel:news_list'))
        self.assertEqual(response.status_code, 302)
    
    def test_news_list_view_no_profile(self):
        user_no_profile = User.objects.create_user(username='noprofile', password='testpass123')
        self.client.login(username='noprofile', password='testpass123')
        response = self.client.get(reverse('artikel:news_list'))
        self.assertEqual(response.status_code, 302)
    
    def test_news_create_view_post_valid(self):
        self.client.login(username='penyedia', password='testpass123')
        form_data = {
            'title': 'Test News',
            'content': 'Test content',
            'kategori': 'Futsal'
        }
        image_file = self._make_image_file()
        response = self.client.post(reverse('artikel:news_create'), {**form_data, 'thumbnail': image_file})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(News.objects.filter(title='Test News').exists())
    
    def test_news_create_view_post_invalid(self):
        self.client.login(username='penyedia', password='testpass123')
        form_data = {
            'title': '',
            'content': '',
            'category': ''
        }
        response = self.client.post(reverse('artikel:news_create'), form_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
    
    def test_news_create_view_user_permission(self):
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'title': 'Test News',
            'content': 'Test content',
            'kategori': 'Futsal'
        }
        response = self.client.post(reverse('artikel:news_create'), form_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('permission', data['errors'])
    
    def test_news_create_view_no_profile(self):
        user_no_profile = User.objects.create_user(username='noprofile', password='testpass123')
        self.client.login(username='noprofile', password='testpass123')
        form_data = {
            'title': 'Test News',
            'content': 'Test content',
            'kategori': 'Futsal'
        }
        response = self.client.post(reverse('artikel:news_create'), form_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
    
    def test_news_update_view_post_valid(self):
        self.client.login(username='penyedia', password='testpass123')
        news = News.objects.create(
            title='Test News',
            content='Test content',
            kategori='Futsal',
            author=self.penyedia,
            thumbnail=self._make_image_file()
        )
        form_data = {
            'title': 'Updated News',
            'content': 'Updated content',
            'kategori': 'Futsal'
        }
        image_file = self._make_image_file()
        response = self.client.post(reverse('artikel:news_update', args=[news.pk]), {**form_data, 'thumbnail': image_file})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        news.refresh_from_db()
        self.assertEqual(news.title, 'Updated News')
    
    def test_news_update_view_wrong_owner(self):
        self.client.login(username='testuser', password='testpass123')
        news = News.objects.create(
            title='Test News',
            content='Test content',
            kategori='Futsal',
            author=self.penyedia,
            thumbnail=self._make_image_file()
        )
        form_data = {
            'title': 'Updated News',
            'content': 'Updated content',
            'kategori': 'Futsal'
        }
        image_file = self._make_image_file()
        response = self.client.post(reverse('artikel:news_update', args=[news.pk]), {**form_data, 'thumbnail': image_file})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
    
    def test_news_delete_view_success(self):
        self.client.login(username='penyedia', password='testpass123')
        news = News.objects.create(
            title='Test News',
            content='Test content',
            kategori='Futsal',
            author=self.penyedia,
            thumbnail=self._make_image_file()
        )
        response = self.client.post(reverse('artikel:news_delete', args=[news.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertFalse(News.objects.filter(id_berita=news.id_berita).exists())
    
    def test_news_delete_view_wrong_owner(self):
        self.client.login(username='testuser', password='testpass123')
        news = News.objects.create(
            title='Test News',
            content='Test content',
            kategori='Futsal',
            author=self.penyedia,
            thumbnail=self._make_image_file()
        )
        response = self.client.post(reverse('artikel:news_delete', args=[news.pk]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
    
    def test_news_public_list_view(self):
        response = self.client.get(reverse('artikel:news_public_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('news_list', response.context)
    
    def test_news_detail_view(self):
        news = News.objects.create(
            title='Test News',
            content='Test content',
            kategori='Futsal',
            author=self.penyedia,
            thumbnail=self._make_image_file()
        )
        response = self.client.get(reverse('artikel:news_detail', args=[news.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['news'], news)
    
    def test_news_detail_view_not_found(self):
        response = self.client.get(reverse('artikel:news_detail', args=[999]))
        self.assertEqual(response.status_code, 404)