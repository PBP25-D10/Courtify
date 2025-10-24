from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import os
import uuid

class Lapangan(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lapangans',
        null=True,    
        blank=True
    )
    id_lapangan = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=255)
    kategori = models.CharField(
        max_length=50,
        choices=[
            ('futsal', 'Futsal'),
            ('basket', 'Basket'),
            ('badminton', 'Badminton'),
            ('tenis', 'Tenis'),
            ('voli', 'Voli'),
            ('lainnya', 'Lainnya'),
        ],
    )
    lokasi = models.CharField(max_length=200)
    harga_per_jam = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    foto = models.ImageField(upload_to="static/img/", blank=True, null=True)
    jam_buka = models.TimeField()
    jam_tutup = models.TimeField()

    
    def __str__(self):
        return self.nama 
