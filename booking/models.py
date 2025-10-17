from django.db import models
from lapangan.models import Lapangan
from django.conf import settings

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,   # tambahkan ini
        blank=True   # tambahkan ini
    )

    lapangan = models.ForeignKey(
        Lapangan,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,   # tambahkan ini
        blank=True   # tambahkan ini
    )

    tanggal = models.DateField()
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.lapangan} ({self.status})"
