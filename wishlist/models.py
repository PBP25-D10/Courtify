from django.conf import settings
from django.db import models
from lapangan.models import Lapangan

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlists'
    )
    lapangan = models.ForeignKey(
        Lapangan,
        on_delete=models.CASCADE,
        related_name='wishlists'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lapangan')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.lapangan.nama}"
