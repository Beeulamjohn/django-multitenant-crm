from django.contrib import admin

from .models import (
    Customer,
    Product,
    CustomerInvoice,
    CustomerPayment,
    CustomerGSTSettings,
)

from .admin_site import customer_admin_site


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "phone",
        "email",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "company__company_name",
    )

    list_filter = (
        "company",
        "created_at",
    )

    ordering = ("name",)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "company",
        "category",
        "price",
        "stock",
        "created_at",
    )

    search_fields = (
        "name",
        "category",
        "company__company_name",
    )

    list_filter = (
        "company",
        "category",
        "created_at",
    )

    ordering = ("name",)


class CustomerInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "company",
        "customer",
        "invoice_date",
        "due_date",
        "total_amount",
        "gst_amount",
        "amount_paid",
        "balance_amount",
        "payment_status",
    )

    search_fields = (
        "invoice_number",
        "customer__name",
        "company__company_name",
    )

    list_filter = (
        "company",
        "payment_status",
        "invoice_date",
        "due_date",
    )

    ordering = (
        "-invoice_date",
    )

    date_hierarchy = "invoice_date"


class CustomerPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_number",
        "company",
        "customer",
        "invoice",
        "payment_date",
        "amount",
        "payment_method",
        "status",
    )

    search_fields = (
        "receipt_number",
        "customer__name",
        "invoice__invoice_number",
        "company__company_name",
    )

    list_filter = (
        "company",
        "payment_method",
        "status",
        "payment_date",
    )

    ordering = (
        "-payment_date",
    )

    date_hierarchy = "payment_date"


class CustomerGSTSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "company_name",
        "gst_number",
        "state",
        "cgst",
        "sgst",
        "igst",
        "is_active",
    )

    search_fields = (
        "company_name",
        "gst_number",
        "state",
        "company__company_name",
    )

    list_filter = (
        "is_active",
        "state",
    )


customer_admin_site.register(Customer, CustomerAdmin)
customer_admin_site.register(Product, ProductAdmin)
customer_admin_site.register(CustomerInvoice, CustomerInvoiceAdmin)
customer_admin_site.register(CustomerPayment, CustomerPaymentAdmin)
customer_admin_site.register(CustomerGSTSettings, CustomerGSTSettingsAdmin)