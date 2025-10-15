from django.db import models

class Iklan(models.Model):
    
    # host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='iklans')
    # lapangan = models.ForeignKey(Lapangan, on_delete=models.CASCADE, related_name='iklans')

    host = models.CharField(max_length=100)
    lapangan = models.CharField(max_length=100)
    date = models.DateField()
    banner = models.ImageField()
