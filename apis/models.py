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
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, blank=True, null=True)
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Country_locales(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Users(models.Model):
    provider = models.CharField(max_length=50, default="email", null=False)
    uid = models.CharField(max_length=50, default="", null=False)
    encrypted_password = models.CharField(max_length=255, default="", null=False)
    reset_password_token = models.CharField(max_length=255, null=True)
    reset_password_sent_at = models.DateTimeField(null=True)
    allow_password_change = models.BooleanField(null=True)
    remember_created_at = models.DateTimeField(null=True)
    confirmation_token = models.CharField(max_length=50, null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True)
    confirmation_sent_at = models.DateTimeField(null=True)
    unconfirmed_email = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    tokens = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sign_in_count = models.IntegerField(default=0)
    current_sign_in_at = models.DateTimeField(null=True)
    last_sign_in_at = models.DateTimeField(null=True)
    current_sign_in_ip = models.CharField(max_length=50, null=True, blank=True)
    last_sign_in_ip = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=50, default="", null=False)
    lastname = models.CharField(max_length=50, default="", null=False)
    phone = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)       # save avatar path
    role_id = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, blank=True, null=True)
    payments_currency = models.IntegerField(default=3, null=False)
    reimbursement_cycle = models.IntegerField(default=0, null=False)


class Images(models.Model):
    user_id = models.IntegerField(default=0)
    avatar = models.ImageField(blank=False, null=False)
    def __str__(self):
        return self.avatar.name

class Reports(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Expenses(models.Model):
    merchant_name = models.CharField(max_length=255, null=True, blank=True)
    receipt_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)
    category = models.IntegerField(null=True, blank=True)
    assignees = models.CharField(max_length=255, null=True, blank=True)
    file_urls = models.TextField(null=True, blank=True)
    file_names = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
    report = models.ForeignKey(Reports, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    currency_type = models.IntegerField(default=3, null=False)
    status = models.IntegerField(default=0, null=False)


class ExpenseFile(models.Model):
    expense_id = models.IntegerField(default=0)
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name


class Industry_locales(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    industry = models.ForeignKey(Industries, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
