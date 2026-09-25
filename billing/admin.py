from django.contrib import admin

from .models import (
    Invoice,
    FeeConfiguration,
    GSTSettings,
    Payment,
    EMI,
)

from .admin_site import billing_admin_site
from .models import BillingSettings



class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "student",
        "company",
        "total_amount",
        "amount_paid",
        "balance_amount",
        "payment_type",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_type",
        "company",
    )

    search_fields = (
        "invoice_number",
        "student__first_name",
        "student__last_name",
        "company__company_name",
    )


class FeeConfigurationAdmin(admin.ModelAdmin):

    list_display = (
        "fee_type",
        "student",
        "course",
        "department",
        "amount",
        "company",
        "created_at",
    )


class GSTSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "gst_number",
        "cgst",
        "sgst",
        "igst",
        "is_active",
    )


class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "receipt_number",
        "student",
        "company",
        "course",
        "amount",
        "payment_method",
        "payment_date",
        "status",
    )


class EMIAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "company",
        "installment_no",
        "amount",
        "due_date",
        "paid_date",
        "status",
    )


# IMPORTANT: register in custom Billing Admin Site

billing_admin_site.register(
    Invoice,
    InvoiceAdmin
)

billing_admin_site.register(
    FeeConfiguration,
    FeeConfigurationAdmin
)

billing_admin_site.register(
    GSTSettings,
    GSTSettingsAdmin
)

billing_admin_site.register(
    Payment,
    PaymentAdmin
)

billing_admin_site.register(
    EMI,
    EMIAdmin
)


@admin.register(BillingSettings)
class BillingSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "currency",
        "financial_year",
        "payment_terms",
        "billing_enabled",
        "default_payment_method",
        "updated_at",
    )

    list_filter = (
        "currency",
        "financial_year",
        "billing_enabled",
        "default_payment_method",
    )

    search_fields = (
        "company__company_name",
    )