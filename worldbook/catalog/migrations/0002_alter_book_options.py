# Generated by Django 5.0.1 on 2024-03-30 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['name'], 'verbose_name': 'Книга', 'verbose_name_plural': 'Книги'},
        ),
    ]
