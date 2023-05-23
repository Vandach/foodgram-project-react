# Generated by Django 3.2.18 on 2023-05-22 13:02

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20230522_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#00ff00', image_field=None, max_length=7, samples=None, unique=True, validators=[django.core.validators.RegexValidator(message='Введите формат HEX. Пример: #00ff00', regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')]),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredien'),
        ),
    ]
