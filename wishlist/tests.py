import uuid
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from lapangan.models import Lapangan
from .models import Wishlist

class TestWishlistViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='12345')
        self.client.login(username='tester', password='12345')
        self.lapangan = Lapangan.objects.create(
            id_lapangan=uuid.uuid4(),
            nama='Lapangan Futsal A',
            kategori='futsal',
            lokasi='Jakarta',
            harga_per_jam=100000,
            owner=self.user
        )

    def test_list_view(self):
        response = self.client.get(reverse('wishlist:wishlist_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist_list.html')

    def test_add_and_remove(self):
        url = reverse('wishlist:wishlist_add', args=[self.lapangan.id_lapangan])
        self.client.get(url)
        self.assertTrue(Wishlist.objects.filter(user=self.user, lapangan=self.lapangan).exists())
        self.client.get(url)
        self.assertFalse(Wishlist.objects.filter(user=self.user, lapangan=self.lapangan).exists())
