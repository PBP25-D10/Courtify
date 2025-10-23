from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from unittest.mock import patch
import json
import uuid
from datetime import time
from io import BytesIO
from PIL import Image

from .models import Lapangan
from .forms import LapanganForm
from authentication.models import UserProfile


class LapanganModelTest(TestCase):
    """Test cases for Lapangan model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=self.user, role='penyedia')
    
    def test_lapangan_creation(self):
        """Test creating a lapangan instance"""
        lapangan = Lapangan.objects.create(
            owner=self.user,
            nama='Lapangan Futsal ABC',
            deskripsi='Lapangan futsal berkualitas tinggi',
            kategori='futsal',
            lokasi='Jl. Contoh No. 123',
            harga_per_jam=50000,
            jam_buka=time(8, 0),
            jam_tutup=time(22, 0)
        )
        
        self.assertEqual(lapangan.nama, 'Lapangan Futsal ABC')
        self.assertEqual(lapangan.owner, self.user)
        self.assertEqual(lapangan.kategori, 'futsal')
        self.assertEqual(lapangan.harga_per_jam, 50000)
        self.assertIsNotNone(lapangan.id_lapangan)
        self.assertIsInstance(lapangan.id_lapangan, uuid.UUID)
        
    def test_lapangan_str_representation(self):
        """Test string representation of lapangan"""
        lapangan = Lapangan.objects.create(
            owner=self.user,
            nama='Lapangan Basket XYZ',
            deskripsi='Lapangan basket indoor',
            kategori='basket',
            lokasi='Jl. Olahraga No. 456',
            harga_per_jam=75000,
            jam_buka=time(9, 0),
            jam_tutup=time(21, 0)
        )
        
        self.assertEqual(str(lapangan), 'Lapangan Basket XYZ')
        
    def test_lapangan_without_owner(self):
        """Test creating lapangan without owner"""
        lapangan = Lapangan.objects.create(
            nama='Lapangan Umum',
            deskripsi='Lapangan untuk umum',
            kategori='badminton',
            lokasi='Jl. Umum No. 789',
            harga_per_jam=30000,
            jam_buka=time(7, 0),
            jam_tutup=time(23, 0)
        )
        
        self.assertIsNone(lapangan.owner)
        self.assertEqual(lapangan.nama, 'Lapangan Umum')
        
    def test_lapangan_kategori_choices(self):
        """Test lapangan kategori choices"""
        valid_categories = ['futsal', 'basket', 'badminton', 'tenis', 'voli', 'lainnya']
        
        for kategori in valid_categories:
            lapangan = Lapangan.objects.create(
                nama=f'Lapangan {kategori.title()}',
                deskripsi=f'Deskripsi {kategori}',
                kategori=kategori,
                lokasi='Jl. Test',
                harga_per_jam=40000,
                jam_buka=time(8, 0),
                jam_tutup=time(20, 0)
            )
            self.assertEqual(lapangan.kategori, kategori)


class LapanganFormTest(TestCase):
    """Test cases for LapanganForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=self.user, role='penyedia')
    
    def _make_image_file(self, name="test.png"):
        """Helper to create test image file"""
        buffer = BytesIO()
        image = Image.new("RGB", (1, 1), color=(255, 0, 0))
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type="image/png")
        
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'nama': 'Lapangan Test',
            'deskripsi': 'Deskripsi lapangan test',
            'kategori': 'futsal',
            'lokasi': 'Jl. Test No. 123',
            'harga_per_jam': 50000,
            'jam_buka': '08:00',
            'jam_tutup': '22:00'
        }
        image_file = self._make_image_file()
        form = LapanganForm(data=form_data, files={"foto": image_file})
        self.assertTrue(form.is_valid())
        
    def test_invalid_jam_tutup_before_jam_buka(self):
        """Test form validation when jam_tutup is before jam_buka"""
        form_data = {
            'nama': 'Lapangan Test',
            'deskripsi': 'Deskripsi lapangan test',
            'kategori': 'futsal',
            'lokasi': 'Jl. Test No. 123',
            'harga_per_jam': 50000,
            'jam_buka': '22:00',
            'jam_tutup': '08:00'  
        }
        image_file = self._make_image_file()
        form = LapanganForm(data=form_data, files={"foto": image_file})
        self.assertFalse(form.is_valid())
        self.assertIn('Jam tutup harus lebih besar dari jam buka.', str(form.errors))
        
    def test_form_fields_required(self):
        """Test that required fields are properly validated"""
        form = LapanganForm(data={})
        self.assertFalse(form.is_valid())
        
        required_fields = ['nama', 'deskripsi', 'kategori', 'lokasi', 'harga_per_jam', 'jam_buka', 'jam_tutup']
        for field in required_fields:
            self.assertIn(field, form.errors)


class LapanganViewsTest(TestCase):
    """Test cases for Lapangan views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        UserProfile.objects.create(user=self.user, role='penyedia')
        UserProfile.objects.create(user=self.other_user, role='penyedia')
    
    def _make_image_file(self, name="test.png"):
        """Helper to create test image file"""
        buffer = BytesIO()
        image = Image.new("RGB", (1, 1), color=(255, 0, 0))
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return SimpleUploadedFile(name, buffer.read(), content_type="image/png")
    
    def _create_test_lapangan(self):
        """Helper to create test lapangan"""
        image_file = self._make_image_file("seed.png")
        form = LapanganForm(data={
            'nama': 'Lapangan Test',
            'deskripsi': 'Deskripsi lapangan test',
            'kategori': 'futsal',
            'lokasi': 'Jl. Test No. 123',
            'harga_per_jam': 50000,
            'jam_buka': '08:00',
            'jam_tutup': '22:00'
        }, files={'foto': image_file})
        assert form.is_valid(), form.errors
        lapangan = form.save(commit=False)
        lapangan.owner = self.user
        lapangan.save()
        return lapangan
        
    def test_manajemen_dashboard_view_authenticated(self):
        """Test manajemen dashboard view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('manajemen_lapangan:manajemen_dashboard'))
        self.assertEqual(response.status_code, 200)
        
    def test_manajemen_dashboard_view_unauthenticated(self):
        """Test manajemen dashboard view for unauthenticated user"""
        response = self.client.get(reverse('manajemen_lapangan:manajemen_dashboard'))
        self.assertIn(response.status_code, [302, 403])
        
    def test_lapangan_list_view_ajax(self):
        """Test lapangan list view with AJAX request"""
        self.client.login(username='testuser', password='testpass123')
        lapangan = self._create_test_lapangan()
        
        response = self.client.get(
            reverse('manajemen_lapangan:lapangan_list_owner'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('lapangan_list', data)
        self.assertEqual(len(data['lapangan_list']), 1)
        self.assertEqual(data['lapangan_list'][0]['nama'], 'Lapangan Test')
        
    def test_lapangan_create_view_get(self):
        """Test lapangan create view GET request"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('manajemen_lapangan:lapangan_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LapanganForm)
        
    def test_lapangan_create_view_post_valid(self):
        """Test lapangan create view POST with valid data"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'nama': 'Lapangan Baru',
            'deskripsi': 'Deskripsi lapangan baru',
            'kategori': 'basket',
            'lokasi': 'Jl. Baru No. 456',
            'harga_per_jam': 60000,
            'jam_buka': '09:00',
            'jam_tutup': '21:00'
        }
        image_file = self._make_image_file()
        response = self.client.post(reverse('manajemen_lapangan:lapangan_create'), {**form_data, 'foto': image_file})
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        
        new_lapangan = Lapangan.objects.get(nama='Lapangan Baru')
        self.assertEqual(new_lapangan.owner, self.user)
        
    def test_lapangan_create_view_post_ajax_valid(self):
        """Test lapangan create view POST with AJAX and valid data"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'nama': 'Lapangan AJAX',
            'deskripsi': 'Deskripsi lapangan AJAX',
            'kategori': 'badminton',
            'lokasi': 'Jl. AJAX No. 789',
            'harga_per_jam': 40000,
            'jam_buka': '07:00',
            'jam_tutup': '23:00'
        }
        image_file = self._make_image_file()
        response = self.client.post(
            reverse('manajemen_lapangan:lapangan_create'),
            {**form_data, 'foto': image_file},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertIn('lapangan', data)
        
    def test_lapangan_edit_view_get(self):
        """Test lapangan edit view GET request"""
        self.client.login(username='testuser', password='testpass123')
        lapangan = self._create_test_lapangan()
        
        response = self.client.get(
            reverse('manajemen_lapangan:lapangan_edit', args=[lapangan.id_lapangan])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LapanganForm)
        
    def test_lapangan_edit_view_post_valid(self):
        """Test lapangan edit view POST with valid data"""
        self.client.login(username='testuser', password='testpass123')
        lapangan = self._create_test_lapangan()
        
        form_data = {
            'nama': 'Lapangan Updated',
            'deskripsi': 'Deskripsi lapangan updated',
            'kategori': 'voli',
            'lokasi': 'Jl. Updated No. 999',
            'harga_per_jam': 70000,
            'jam_buka': '10:00',
            'jam_tutup': '20:00'
        }
        image_file = self._make_image_file()
        response = self.client.post(
            reverse('manajemen_lapangan:lapangan_edit', args=[lapangan.id_lapangan]),
            {**form_data, 'foto': image_file}
        )
        self.assertEqual(response.status_code, 302)  
        
        updated_lapangan = Lapangan.objects.get(id_lapangan=lapangan.id_lapangan)
        self.assertEqual(updated_lapangan.nama, 'Lapangan Updated')
        self.assertEqual(updated_lapangan.kategori, 'voli')
        
    def test_lapangan_delete_view_post_ajax_success(self):
        """Test lapangan delete view POST with AJAX for owner"""
        self.client.login(username='testuser', password='testpass123')
        lapangan = self._create_test_lapangan()
        
        response = self.client.post(
            reverse('manajemen_lapangan:lapangan_delete', args=[lapangan.id_lapangan]),
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        
        # Check if lapangan was deleted
        self.assertFalse(Lapangan.objects.filter(id_lapangan=lapangan.id_lapangan).exists())
        
    def test_lapangan_delete_view_post_ajax_unauthorized(self):
        """Test lapangan delete view POST with AJAX for non-owner"""
        self.client.login(username='otheruser', password='otherpass123')
        lapangan = self._create_test_lapangan()
        
        response = self.client.post(
            reverse('manajemen_lapangan:lapangan_delete', args=[lapangan.id_lapangan]),
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 403)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        
        self.assertTrue(Lapangan.objects.filter(id_lapangan=lapangan.id_lapangan).exists())
        
    def test_lapangan_create_view_post_ajax_invalid(self):
        """Test lapangan create view POST with AJAX and invalid data"""
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'nama': '',  
            'deskripsi': 'Deskripsi lapangan',
            'kategori': 'futsal',
            'lokasi': 'Jl. Test',
            'harga_per_jam': 50000,
            'jam_buka': '22:00',
            'jam_tutup': '08:00'  
        }
        image_file = self._make_image_file()
        response = self.client.post(
            reverse('manajemen_lapangan:lapangan_create'),
            {**form_data, 'foto': image_file},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')
        self.assertIn('message', data)