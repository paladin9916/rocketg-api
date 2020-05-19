# Generated by Django 2.2.7 on 2020-02-16 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0011_users_special_privilege'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='special_privilege',
        ),
        migrations.AddField(
            model_name='companies',
            name='approve_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='companies',
            name='open_user_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='companies',
            name='processing_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='companies',
            name='reimburse_id',
            field=models.IntegerField(null=True),
        ),
    ]
