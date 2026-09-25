from datetime import timedelta
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):

    COMPANY_TYPES = (
        ("education", "Education"),
        ("billing", "Billing"),
        ("customer", "Customer"),
        ("employee", "Employee"),
        ("salary", "Salary"),
    )

    ROLE_CHOICES = (
        ("company_admin", "Company Admin"),
        ("staff", "Staff"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company",
    )

    company_name = models.CharField(max_length=200)

    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    full_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    company_type = models.CharField(
        max_length=30,
        choices=COMPANY_TYPES,
        default="education"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="company_admin"
    )

    # NEW FIELD (Billing → Education Link)
    linked_education_company = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_billing_companies",
        limit_choices_to={"company_type": "education"},
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

class SubscriptionPlan(models.Model):

    PLAN_CHOICES = (
    ("Starter", "Starter"),
    ("Professional", "Professional"),
    ("Enterprise", "Enterprise"),
)
    name = models.CharField(
        max_length=30,
        choices=PLAN_CHOICES,
        unique=True,
    )

    monthly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    yearly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    trial_days = models.PositiveIntegerField(
        default=14
    )

    max_customers = models.PositiveIntegerField(
        default=100
    )

    max_employees = models.PositiveIntegerField(
        default=10
    )

    def __str__(self):
        return self.name


class CompanySubscription(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )

    start_date = models.DateField(
        default=timezone.now
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    is_trial = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def save(self, *args, **kwargs):

        if self.end_date is None:
            self.end_date = (
                self.start_date
                + timedelta(days=self.plan.trial_days)
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company.company_name} - {self.plan.name}"


class Payment(models.Model):

    PAYMENT_METHODS = (
        ("Razorpay", "Razorpay"),
        ("Stripe", "Stripe"),
    )

    PAYMENT_STATUS = (
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="saas_payments",
    )

    subscription = models.ForeignKey(
        CompanySubscription,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
    )

    transaction_id = models.CharField(
        max_length=200,
        unique=True,
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending",
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.transaction_id


class ContactSales(models.Model):

    name = models.CharField(
        max_length=100
    )

    company = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    employees = models.CharField(
        max_length=50
    )

    message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.company


class PasswordResetToken(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens"
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(
        default=False
    )

    def is_valid(self):

        return (
            not self.is_used
            and timezone.now() < self.expires_at
        )

    def __str__(self):

        return f"Password reset - {self.user.username}"