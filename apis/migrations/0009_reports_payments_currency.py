# Generated by Django 2.2.7 on 2020-01-16 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0008_expenses_payments_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='payments_currency',
            field=models.IntegerField(default=3),
        ),
    ]