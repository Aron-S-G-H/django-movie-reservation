# Generated by Django 5.1.2 on 2024-10-30 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0005_reservation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ['-created_at']},
        ),
    ]