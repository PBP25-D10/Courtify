from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    KATEGORI_CHOICES = [
        ('Futsal', 'Futsal'),
        ('Basket', 'Basket'),
        ('Badminton', 'Badminton'),
        ('Tenis', 'Tenis'),
        ('Padel', 'Padel'),
        ('Komunitas', 'Komunitas'),
        ('Tips', 'Tips Olahraga'),
    ]

    id_berita = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

