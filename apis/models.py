from django.db import models


class Countries(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Industries(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Companies(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    active_employees = models.IntegerField(default=0)
    total_expenses = models.IntegerField(default=0)
    manage = models.CharField(max_length=50, null=False, blank=True)
    website = models.CharField(max_length=50, null=False, blank=True)
    employee_count_index = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, blank=True, null=True)
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE, blank=True, null=True)


class Country_locales(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, blank=True, null=True)


class Users(models.Model):
    provider = models.CharField(max_length=50, default="email", null=False)
    uid = models.CharField(max_length=50, default="", null=False)
    encrypted_password = models.CharField(max_length=50, default="", null=False)
    reset_password_token = models.CharField(max_length=50, default="", null=False)
    reset_password_sent_at = models.DateTimeField()
    allow_password_change = models.BooleanField(default=False)
    remember_created_at = models.DateTimeField()
    confirmation_token = models.CharField(max_length=50, null=True, blank=True)
    confirmed_at = models.DateTimeField()
    confirmation_sent_at = models.DateTimeField()
    unconfirmed_email = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    tokens = models.CharField(max_length=255, null=True, blank=True)
    sign_in_count = models.IntegerField(default=0)
    current_sign_in_at = models.DateTimeField()
    last_sign_in_at = models.DateTimeField()
    current_sign_in_ip = models.CharField(max_length=50, null=True, blank=True)
    last_sign_in_ip = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=50, default="", null=False)
    lastname = models.CharField(max_length=50, default="", null=False)
    phone = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.CharField(max_length=50, null=True, blank=True)
    role_id = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, default="en", null=False)
    reimbursement_cycle = models.IntegerField()
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, blank=True, null=True)
    

class Expenses(models.Model):
    merchant_name = models.CharField(max_length=50, null=False, blank=True)
    receipt_date = models.DateField()
    description = models.CharField(max_length=50, null=False, blank=True)
    total_amount = models.FloatField(default=0.0)
    category = models.IntegerField(default=1)
    assignees = models.CharField(max_length=50, null=False, blank=True)
    file_urls = models.CharField(max_length=255, null=True, blank=True)
    file_names = models.CharField(max_length=255, null=True, blank=True)
    currency_type = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)


class Industry_locales(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE, blank=True, null=True)


