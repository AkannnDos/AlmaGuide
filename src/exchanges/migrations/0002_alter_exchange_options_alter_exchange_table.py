# Generated by Django 5.0.3 on 2024-04-26 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchanges', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exchange',
            options={'ordering': ('currency',), 'verbose_name': 'Exchange', 'verbose_name_plural': 'Exchanges'},
        ),
        migrations.AlterModelTable(
            name='exchange',
            table='exchange',
        ),
    ]
