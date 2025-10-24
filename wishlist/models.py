from django.conf import settings
from django.db import models
from main.models import Iklan

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlists'
    )
    iklan = models.ForeignKey(
        Iklan,
        on_delete=models.CASCADE,
        related_name='wishlists',
        default=1
    )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'iklan')
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.user.username} - {self.iklan.judul}"

