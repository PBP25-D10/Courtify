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

    judul = models.CharField(max_length=100, default="New Ad!")
    deskripsi = models.TextField(default="Click to see details..")
    banner = models.ImageField(upload_to='iklan_banners/', blank=True, null=True)
    url_thumbnail = models.URLField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    # Urutan berdasarkan iklan terbaru
    class Meta:
        ordering = ['-date']

    # Return banner kalau ada, return foto lapangan kalau tidak ada banner
    def get_banner_url(self):
        if self.banner:
            return self.banner.url
        
        elif self.lapangan and self.lapangan.foto:
            return self.lapangan.foto.url
    
