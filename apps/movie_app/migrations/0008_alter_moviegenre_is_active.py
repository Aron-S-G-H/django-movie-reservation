# Generated by Django 5.1.2 on 2024-11-05 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0007_reservation_user_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviegenre',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
