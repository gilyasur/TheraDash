# Generated by Django 5.0.1 on 2024-03-01 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]