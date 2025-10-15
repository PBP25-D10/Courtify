from django.db import models

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    # nanti ini akan dihubungkan ke model User dan Lapangan
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    # lapangan = models.ForeignKey(Lapangan, on_delete=models.CASCADE, related_name='bookings')

    nama_pemesan = models.CharField(max_length=100)   # sementara ganti user dengan nama manual
    nama_lapangan = models.CharField(max_length=100)  # sementara ganti model Lapangan dengan string

    tanggal = models.DateField()
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_pemesan} - {self.nama_lapangan} ({self.status})"
