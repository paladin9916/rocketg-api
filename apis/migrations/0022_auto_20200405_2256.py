# Generated by Django 2.2.7 on 2020-04-05 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0021_auto_20200405_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paylips',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
