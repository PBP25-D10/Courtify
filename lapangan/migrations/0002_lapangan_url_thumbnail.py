from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapangan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lapangan',
            name='url_thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
