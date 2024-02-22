# Generated by Django 5.0.1 on 2024-01-17 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_appointment_canceled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='cancellation_reason',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
