# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('penyedia', 'Penyedia'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # ... field lainnya seperti phone, address, dll.

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"