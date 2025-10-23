from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta

from booking.models import Booking
from lapangan.models import Lapangan
from booking.forms import BookingForm
from authentication.models import UserProfile


class BookingViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.penyedia = User.objects.create_user(username='penyedia', password='testpass123')
        UserProfile.objects.create(user=self.user, role='user')
        UserProfile.objects.create(user=self.penyedia, role='penyedia')
        
        self.lapangan = Lapangan.objects.create(
            nama='Lapangan Test',
            deskripsi='Test deskripsi',
            kategori='futsal',
            lokasi='Jl. Test',
            harga_per_jam=50000,
            jam_buka='08:00',
            jam_tutup='22:00'
        )
    
    def test_booking_dashboard_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking:booking_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_booking_dashboard_view_unauthenticated(self):
        response = self.client.get(reverse('booking:booking_dashboard'))
        self.assertIn(response.status_code, [302, 403])
    
    def test_booking_dashboard_view_ajax(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('booking:booking_dashboard'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('bookings', data)
    
    def test_booking_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking:booking_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('lapangan_list', response.context)
    
    def test_booking_create_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking:booking_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], BookingForm)
    
    def test_booking_create_view_get_with_lapangan(self):
        self.client.login(username='testuser', password='testpass123')
        url = f"{reverse('booking:booking_create')}?lapangan_id={self.lapangan.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_booking_create_view_post_valid(self):
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'lapangan': self.lapangan.id,
            'tanggal': '2024-12-31',
            'jam_mulai': '10:00',
            'jam_selesai': '12:00',
            'status': 'pending'
        }
        response = self.client.post(reverse('booking:booking_create'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.filter(user=self.user).exists())
    
    def test_booking_create_view_post_invalid(self):
        self.client.login(username='testuser', password='testpass123')
        form_data = {
            'lapangan': '',
            'tanggal': '',
            'jam_mulai': '',
            'jam_selesai': ''
        }
        response = self.client.post(reverse('booking:booking_create'), form_data)
        self.assertEqual(response.status_code, 200)
    
    def test_update_booking_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        booking = Booking.objects.create(
            user=self.user,
            lapangan=self.lapangan,
            tanggal='2024-12-31',
            jam_mulai='10:00',
            jam_selesai='12:00'
        )
        response = self.client.get(reverse('booking:update_booking', args=[booking.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_update_booking_view_post_valid(self):
        self.client.login(username='testuser', password='testpass123')
        booking = Booking.objects.create(
            user=self.user,
            lapangan=self.lapangan,
            tanggal='2024-12-31',
            jam_mulai='10:00',
            jam_selesai='12:00'
        )
        form_data = {
            'lapangan': self.lapangan.id,
            'tanggal': '2024-12-31',
            'jam_mulai': '14:00',
            'jam_selesai': '16:00',
            'status': 'confirmed'
        }
        response = self.client.post(reverse('booking:update_booking', args=[booking.pk]), form_data)
        self.assertEqual(response.status_code, 302)
    
    def test_update_booking_view_post_ajax(self):
        self.client.login(username='testuser', password='testpass123')
        booking = Booking.objects.create(
            user=self.user,
            lapangan=self.lapangan,
            tanggal='2024-12-31',
            jam_mulai='10:00',
            jam_selesai='12:00'
        )
        form_data = {
            'lapangan': self.lapangan.id,
            'tanggal': '2024-12-31',
            'jam_mulai': '14:00',
            'jam_selesai': '16:00',
            'status': 'confirmed'
        }
        response = self.client.post(
            reverse('booking:update_booking', args=[booking.pk]),
            form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
    
    def test_cancel_booking_view(self):
        self.client.login(username='testuser', password='testpass123')
        booking = Booking.objects.create(
            user=self.user,
            lapangan=self.lapangan,
            tanggal='2024-12-31',
            jam_mulai='10:00',
            jam_selesai='12:00'
        )
        response = self.client.post(reverse('booking:cancel_booking', args=[booking.pk]))
        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')
    
    def test_cancel_booking_view_ajax(self):
        self.client.login(username='testuser', password='testpass123')
        booking = Booking.objects.create(
            user=self.user,
            lapangan=self.lapangan,
            tanggal='2024-12-31',
            jam_mulai='10:00',
            jam_selesai='12:00'
        )
        response = self.client.post(
            reverse('booking:cancel_booking', args=[booking.pk]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
    
    def test_booking_unauthorized_access(self):
        self.client.login(username='testuser', password='testpass123')
        other_user = User.objects.create_user(username='other', password='testpass123')
        booking = Booking.objects.create(
            user=other_user,
            lapangan=self.lapangan,
            tanggal='2024-12-31',
            jam_mulai='10:00',
            jam_selesai='12:00'
        )
        response = self.client.get(reverse('booking:update_booking', args=[booking.pk]))
        self.assertEqual(response.status_code, 404)