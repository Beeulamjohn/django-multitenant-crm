from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Company,
    SubscriptionPlan,
    CompanySubscription,
    Payment,
    ContactSales,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "logo_preview",
        "company_name",
        "company_type",
        "linked_education_company",
        "full_name",
        "phone",
        "user",
        "is_active",
    )

    list_filter = (
        "company_type",
        "is_active",
    )

    search_fields = (
        "company_name",
        "full_name",
        "phone",
        "user__username",
    )

    readonly_fields = ("logo_preview",)

    fieldsets = (
        ("Company Information", {
            "fields": (
                "company_name",
                "company_type",
                "linked_education_company",
                "full_name",
                "phone",
                "user",
                "logo",
                "logo_preview",
                "is_active",
            )
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="border-radius:50%; object-fit:cover;" />',
                obj.logo.url
            )
        return "No Logo"

    logo_preview.short_description = "Logo"




@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "monthly_price",
        "yearly_price",
        "trial_days",
        "max_customers",
        "max_employees",
    )


@admin.register(CompanySubscription)
class CompanySubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "plan",
        "start_date",
        "end_date",
        "is_trial",
        "is_active",
    )

    list_filter = (
        "is_trial",
        "is_active",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "company",
        "amount",
        "payment_method",
        "status",
        "payment_date",
    )
    list_filter = (
        "status",
        "payment_method",
    )
    search_fields = (
        "transaction_id",
    )


@admin.register(ContactSales)
class ContactSalesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "email",
        "phone",
        "employees",
        "created_at",
    )
    search_fields = (
        "name",
        "company",
        "email",
    )
    list_filter = (
        "employees",
        "created_at",
    )