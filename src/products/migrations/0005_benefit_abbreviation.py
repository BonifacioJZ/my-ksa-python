# Generated by Django 4.2.19 on 2025-02-13 20:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_benefit_slug_alter_brand_slug_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefit',
            name='abbreviation',
            field=models.CharField(default=django.utils.timezone.now, max_length=5, verbose_name='Abreviatura'),
            preserve_default=False,
        ),
    ]
