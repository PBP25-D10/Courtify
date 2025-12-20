from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artikel', '0002_url_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
    ]
