# Generated by Django 3.2.12 on 2024-10-08 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('samlskrammel', '0002_auto_20241007_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='myWeight',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=10),
            preserve_default=False,
        ),
    ]