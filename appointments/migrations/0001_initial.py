# Generated by Django 4.1.7 on 2023-03-01 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('appointment_status', models.CharField(choices=[('ACTIVE', 'Active'), ('CANCELED', 'Canceled'), ('COMPLETE', 'Complete')], max_length=10)),
            ],
        ),
    ]
