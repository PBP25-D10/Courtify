import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id_berita', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('kategori', models.CharField(choices=[('Futsal', 'Futsal'), ('Basket', 'Basket'), ('Badminton', 'Badminton'), ('Tenis', 'Tenis'), ('Padel', 'Padel'), ('Komunitas', 'Komunitas'), ('Tips', 'Tips Olahraga')], max_length=50)),
                ('thumbnail', models.ImageField(upload_to='thumbnails/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
