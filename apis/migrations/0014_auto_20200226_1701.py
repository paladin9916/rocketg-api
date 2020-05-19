# Generated by Django 2.2.7 on 2020-02-26 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0013_auto_20200226_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companies',
            name='user_id',
        ),
        migrations.AddField(
            model_name='companies',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_user', to='apis.Users'),
        ),
    ]
