from django.utils import timezone
from django.conf import settings
from django.db import models
from lapangan.models import Lapangan

class Iklan(models.Model):
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='iklans'
    )
    lapangan = models.ForeignKey(
        Lapangan,
        on_delete=models.CASCADE,
        related_name='iklans'
    )
    banner = models.ImageField(upload_to='iklan_banners/')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date'] #Urutan berdasarkan iklan terbaru