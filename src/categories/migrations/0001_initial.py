# Generated by Django 5.0.3 on 2024-04-02 21:00

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('name_en', models.CharField(max_length=255, verbose_name='Name EN')),
                ('name_ru', models.CharField(max_length=255, verbose_name='Name RU')),
                ('name_kk', models.CharField(max_length=255, verbose_name='Name KK')),
                ('icon', models.ImageField(upload_to='icons/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico'])])),
                ('is_popular', models.BooleanField(default=False, help_text='Only 8 categories can be popular', verbose_name='Is popular')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('name_en', models.CharField(max_length=255, verbose_name='Name EN')),
                ('name_ru', models.CharField(max_length=255, verbose_name='Name RU')),
                ('name_kk', models.CharField(max_length=255, verbose_name='Name KK')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='categories.category', verbose_name='Caregory')),
            ],
            options={
                'verbose_name': 'Subcategory',
                'verbose_name_plural': 'Subcategories',
                'db_table': 'subcategory',
            },
        ),
    ]
