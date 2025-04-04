# Generated by Django 5.1.7 on 2025-03-30 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moysklad', '0003_alter_moyskladproduct_price2_currency_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moyskladproduct',
            options={'verbose_name': 'Товар МойСклад', 'verbose_name_plural': 'Товары МойСклад'},
        ),
        migrations.AddField(
            model_name='moyskladproduct',
            name='aka',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='article',
            field=models.CharField(blank=True, max_length=100, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='barcodes',
            field=models.JSONField(default=list, verbose_name='Штрихкоды'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='code',
            field=models.CharField(blank=True, max_length=100, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='meta',
            field=models.JSONField(verbose_name='Метаданные'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='payment_item_type',
            field=models.CharField(max_length=50, verbose_name='Тип оплаты'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='price2_currency',
            field=models.CharField(blank=True, max_length=3, verbose_name='Валюта цены 2'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='price2_type',
            field=models.CharField(blank=True, max_length=100, verbose_name='Тип цены 2'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='price2_value',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, verbose_name='Цена 2'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='price_currency',
            field=models.CharField(blank=True, max_length=3, verbose_name='Валюта цены'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='price_type',
            field=models.CharField(blank=True, max_length=100, verbose_name='Тип цены'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='price_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='vat',
            field=models.IntegerField(default=0, verbose_name='НДС'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='vat_enabled',
            field=models.BooleanField(default=False, verbose_name='НДС включен'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='volume',
            field=models.FloatField(default=0.0, verbose_name='Объем'),
        ),
        migrations.AlterField(
            model_name='moyskladproduct',
            name='weight',
            field=models.FloatField(default=0.0, verbose_name='Вес'),
        ),
    ]
