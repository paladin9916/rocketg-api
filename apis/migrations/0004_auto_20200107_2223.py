# Generated by Django 2.2.7 on 2020-01-07 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_expenses_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='reimbursement_cycle',
        ),
        migrations.AlterField(
            model_name='users',
            name='payments_currency',
            field=models.IntegerField(default=3),
        ),
    ]
