# Generated by Django 2.2.7 on 2020-03-29 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0019_auto_20200323_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='companies',
            name='step_users',
            field=models.IntegerField(default=0),
        ),
    ]
