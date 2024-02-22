# Generated by Django 5.0.1 on 2024-01-17 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_appointment_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='is_active',
        ),
        migrations.AddField(
            model_name='appointment',
            name='canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appointment',
            name='cancellation_reason',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
