# Generated by Django 4.2.19 on 2025-02-17 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0002_supplier_slug_suppliercontact_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Whatsapp'),
        ),
        migrations.AddField(
            model_name='suppliercontact',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Whatsapp'),
        ),
    ]
