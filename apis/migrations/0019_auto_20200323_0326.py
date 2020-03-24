# Generated by Django 2.2.7 on 2020-03-23 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0018_users_reporter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='approve_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_approve_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='companies',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apis.Countries'),
        ),
        migrations.AlterField(
            model_name='companies',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apis.Industries'),
        ),
        migrations.AlterField(
            model_name='companies',
            name='open_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_open_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='companies',
            name='processing_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_processing_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='companies',
            name='reimburse_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_reimburse_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='companies',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='country_locales',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apis.Countries'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='approve_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_approve_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apis.Companies'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='open_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_open_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='processing_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_processing_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='reimburse_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_reimburse_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apis.Reports'),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expense_user', to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='industry_locales',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apis.Industries'),
        ),
        migrations.AlterField(
            model_name='reports',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apis.Users'),
        ),
        migrations.AlterField(
            model_name='users',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apis.Companies'),
        ),
    ]
