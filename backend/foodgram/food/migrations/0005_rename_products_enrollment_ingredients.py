# Generated by Django 3.2.18 on 2023-04-14 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_rename_ammount_enrollment_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrollment',
            old_name='products',
            new_name='ingredients',
        ),
    ]