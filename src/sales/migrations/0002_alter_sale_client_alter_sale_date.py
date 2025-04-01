# Generated by Django 4.2.19 on 2025-04-01 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_client_phone'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
