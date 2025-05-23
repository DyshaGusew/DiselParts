# Generated by Django 5.1.7 on 2025-04-20 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoyskladProduct',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('aka', models.CharField(blank=True, max_length=200, null=True, verbose_name='Наименование')),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('moysklad_url', models.URLField(blank=True, help_text='Прямая ссылка на товар в интерфейсе МойСклад', max_length=500, verbose_name='Ссылка в МойСклад')),
                ('code', models.CharField(blank=True, max_length=100, verbose_name='Код')),
                ('article', models.CharField(blank=True, max_length=100, verbose_name='Артикул')),
                ('external_code', models.CharField(blank=True, max_length=100, verbose_name='Внешний код')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('vat', models.IntegerField(default=0, verbose_name='НДС')),
                ('effective_vat', models.IntegerField(blank=True, default=0, verbose_name='Эффективный НДС')),
                ('effective_vat_enabled', models.BooleanField(default=False, verbose_name='Эффективный НДС включен')),
                ('vat_enabled', models.BooleanField(default=False, verbose_name='НДС включен')),
                ('archived', models.BooleanField(default=False, verbose_name='В архиве')),
                ('weight', models.FloatField(blank=True, default=0.0, verbose_name='Вес')),
                ('volume', models.FloatField(blank=True, default=0.0, verbose_name='Объем')),
                ('minimum_balance', models.FloatField(blank=True, default=0.0, verbose_name='Минимальный остаток')),
                ('barcodes', models.JSONField(blank=True, default=list, verbose_name='Штрихкоды')),
                ('payment_item_type', models.CharField(default='GOOD', max_length=50, verbose_name='Тип оплаты')),
                ('price_value', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Цена')),
                ('price_type', models.CharField(blank=True, max_length=100, verbose_name='Тип цены')),
                ('min_price_value', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, verbose_name='Минимальная цена')),
                ('buy_price_value', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, verbose_name='Закупочная цена')),
                ('product_folder_name', models.CharField(blank=True, default='Основная', max_length=255, verbose_name='Название группы')),
                ('product_folder_description', models.TextField(blank=True, verbose_name='Описание группы')),
                ('country_name', models.CharField(blank=True, max_length=100, verbose_name='Страна')),
                ('supplier_legal_title', models.CharField(blank=True, max_length=255, verbose_name='Поставщик')),
                ('supplier_actual_address', models.TextField(blank=True, verbose_name='Фактический адрес поставщика')),
                ('supplier_phone', models.CharField(blank=True, max_length=50, verbose_name='Телефон поставщика')),
                ('images', models.JSONField(blank=True, default=list, verbose_name='Изображения')),
            ],
            options={
                'verbose_name': 'Товар МойСклад',
                'verbose_name_plural': 'Товары МойСклад',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='moysklad_mo_name_cc5561_idx'), models.Index(fields=['article'], name='moysklad_mo_article_18c6de_idx'), models.Index(fields=['code'], name='moysklad_mo_code_76f482_idx'), models.Index(fields=['price_value'], name='moysklad_mo_price_v_37bc6a_idx'), models.Index(fields=['archived'], name='moysklad_mo_archive_009815_idx')],
            },
        ),
    ]
