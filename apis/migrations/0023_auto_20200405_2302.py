# Generated by Django 2.2.7 on 2020-04-05 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0022_auto_20200405_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='paylips_count_index',
            new_name='paylips_count',
        ),
    ]
