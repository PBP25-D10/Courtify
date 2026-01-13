from django.db import models
from django.core.validators import MinValueValidator
import os 
import uuid
# Create your models here.

class Lapangan(models.Model):
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
    foto = models.ImageField(upload_to="static/img/")
    jam_buka = models.TimeField()
    jam_tutup = models.TimeField()
