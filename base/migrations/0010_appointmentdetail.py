# Generated by Django 5.0.1 on 2024-01-24 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_appointment_cancellation_reason_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurrence_date', models.DateField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('canceled', models.BooleanField(blank=True, default=False, null=True)),
                ('cancellation_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.appointment')),
            ],
        ),
    ]
