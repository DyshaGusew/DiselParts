# Generated by Django 5.1.7 on 2025-04-20 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('moysklad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductForSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('aka', models.CharField(blank=True, max_length=200, null=True, verbose_name='Наименование')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('article', models.CharField(blank=True, max_length=100, verbose_name='Артикул')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('group', models.CharField(blank=True, max_length=255, verbose_name='Группа')),
                ('country', models.CharField(blank=True, max_length=255, verbose_name='Страна')),
                ('supplier_legal_title', models.CharField(blank=True, max_length=255, verbose_name='Производитель')),
                ('sale_price_moy_sklad', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='Цена продажи мойсклад')),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True, verbose_name='Цена продажи')),
                ('markup_percent', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='Процент наценки')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен для продажи')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Просмотры')),
                ('rating', models.FloatField(default=0.0, verbose_name='Рейтинг')),
                ('moysklad_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='for_sale', to='moysklad.moyskladproduct', verbose_name='Продукт из МойСклад')),
            ],
            options={
                'verbose_name': 'Товар для продажи',
                'verbose_name_plural': 'Товары для продажи',
                'ordering': ['name'],
            },
        ),
    ]
