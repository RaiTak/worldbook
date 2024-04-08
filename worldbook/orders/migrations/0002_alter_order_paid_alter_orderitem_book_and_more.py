# Generated by Django 5.0.1 on 2024-04-08 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_book_options'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Оплачен'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='catalog.book', verbose_name='Книга'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
    ]