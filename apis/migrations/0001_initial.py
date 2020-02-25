# Generated by Django 2.2.7 on 2020-01-07 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('active_employees', models.IntegerField(default=0)),
                ('total_expenses', models.IntegerField(default=0)),
                ('manage', models.CharField(blank=True, max_length=50)),
                ('website', models.CharField(blank=True, max_length=50)),
                ('employee_count_index', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_id', models.IntegerField(default=0)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('avatar', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Industries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(default='email', max_length=50)),
                ('uid', models.CharField(default='', max_length=50)),
                ('encrypted_password', models.CharField(default='', max_length=255)),
                ('reset_password_token', models.CharField(max_length=255, null=True)),
                ('reset_password_sent_at', models.DateTimeField(null=True)),
                ('allow_password_change', models.BooleanField(null=True)),
                ('remember_created_at', models.DateTimeField(null=True)),
                ('confirmation_token', models.CharField(blank=True, max_length=50, null=True)),
                ('confirmed_at', models.DateTimeField(null=True)),
                ('confirmation_sent_at', models.DateTimeField(null=True)),
                ('unconfirmed_email', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('tokens', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sign_in_count', models.IntegerField(default=0)),
                ('current_sign_in_at', models.DateTimeField(null=True)),
                ('last_sign_in_at', models.DateTimeField(null=True)),
                ('current_sign_in_ip', models.CharField(blank=True, max_length=50, null=True)),
                ('last_sign_in_ip', models.CharField(blank=True, max_length=50, null=True)),
                ('firstname', models.CharField(default='', max_length=50)),
                ('lastname', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('job_title', models.CharField(blank=True, max_length=50, null=True)),
                ('department', models.CharField(blank=True, max_length=50, null=True)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('role_id', models.CharField(blank=True, max_length=50, null=True)),
                ('language', models.CharField(max_length=50, null=True)),
                ('reimbursement_cycle', models.IntegerField(null=True)),
                ('payments_currency', models.IntegerField(null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Companies')),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Industry_locales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Industries')),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_name', models.CharField(blank=True, max_length=255, null=True)),
                ('receipt_date', models.DateField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('total_amount', models.FloatField(blank=True, null=True)),
                ('category', models.IntegerField(blank=True, null=True)),
                ('assignees', models.CharField(blank=True, max_length=255, null=True)),
                ('file_urls', models.TextField(blank=True, null=True)),
                ('file_names', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('currency_type', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Companies')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Reports')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Users')),
            ],
        ),
        migrations.CreateModel(
            name='Country_locales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('currency', models.CharField(blank=True, max_length=50, null=True)),
                ('language', models.CharField(blank=True, max_length=50, null=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Countries')),
            ],
        ),
        migrations.AddField(
            model_name='companies',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Countries'),
        ),
        migrations.AddField(
            model_name='companies',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apis.Industries'),
        ),
    ]