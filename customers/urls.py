from django.urls import path
from . import views

urlpatterns = [

    path(
        "product-dashboard/",
        views.product_dashboard,
        name="product_dashboard"
    ),
    path(
        "customer_login/",
        views.customer_login,
        name="customer_login"
    ),
    path(
        "register_customer/",
        views.register_customer,
        name="register_customer"
    ),


    path(
        "customers/",
        views.customer_list,
        name="customer_list"
    ),

    path(
        "customers/add/",
        views.customer_create,
        name="customer_create"
    ),
     path(
        "<int:customer_id>/edit/",
        views.customer_edit,
        name="customer_edit",
    ),

    path(
        "<int:customer_id>/delete/",
        views.customer_delete,
        name="customer_delete",
    ),
  path(
    "payments/<int:pk>/print/",
    views.payment_print,
    name="payment_print",
),
    path(
        "products/",
        views.product_list,
        name="product_list"
    ),
    

    path(
        "products/add/",
        views.product_create,
        name="product_create"
    ),
       path(
        "products/<int:product_id>/edit/",
        views.product_update,
        name="product_update"
    ),

    path(
        "products/<int:product_id>/delete/",
        views.product_delete,
        name="product_delete"
    ),

    path(
        "invoices/",
        views.invoice_list,
        name="invoice_list"
    ),

    path(
        "invoice/create/",
        views.invoice_create,
        name="invoice_create"
    ),
    path(
        "invoice/<int:invoice_id>/",
        views.invoice_view,
        name="invoice_view"
    ),

    path(
        "invoice/<int:invoice_id>/edit/",
        views.invoice_edit,
        name="invoice_edit"
    ),

    path(
        "invoice/<int:invoice_id>/delete/",
        views.invoice_delete,
        name="invoice_delete"
    ),

    path(
        "invoice/<int:invoice_id>/print/",
        views.invoice_print,
        name="invoice_print"
    ),

    path(
        "customer_payment_list/",
        views.customer_payment_list,
        name="customer_payment_list"
    ),

    path(
        "customer_payment_form/",
        views.customer_payment_form,
        name="customer_payment_form"
    ),

   
    path(
        "payment/<int:pk>/edit/",
        views.payment_update,
        name="payment_update"
    ),

    path(
        "payment/<int:pk>/print/",
        views.payment_print,
        name="payment_print"
    ),

    path(
        "payment/<int:pk>/delete/",
        views.payment_delete,
        name="payment_delete"
    ),



    path(
        "reports/",
        views.reports,
        name="reports"
    ),

    path(
        "settings/",
        views.settings,
        name="settings"
    ),

    path(
        "gst_settings_list/",
        views.gst_settings_list,
        name="gst_settings_list"
    ),
    path(
        "gst/delete/<int:pk>/",
        views.delete_gst,
        name="delete_gst"
    ),

    path(
    "product-portal/",
    views.product_portal,
    name="product_portal",
    ),
    path(
    "customer-admin-login/",
    views.customer_admin_login,
    name="customer_admin_login"
),

path(
    "customer-staff-login/",
    views.customer_staff_login,
    name="customer_staff_login"
),

    

    path(
        "customer-billing/settings/",
        views.customer_billing_settings,
        name="customer_billing_settings",
    ),
   
    path(
        "customer-billing/settings/company-profile/",
        views.customer_company_profile,
        name="customer_company_profile",
    ),


    path(
        "customer-billing/settings/invoice/",
        views.customer_invoice_settings,
        name="customer_invoice_settings",
    ),

    path(
        "customer-billing/settings/payment/",
        views.customer_payment_settings,
        name="customer_payment_settings",
    ),

    path(
        "customer-billing/settings/tax-gst/",
        views.customer_tax_gst_settings,
        name="customer_tax_gst_settings",
    ),



    path(
        "customer-billing/settings/discount/",
        views.customer_discount_settings,
        name="customer_discount_settings",
    ),



    path(
        "customer-billing/settings/notifications/",
        views.customer_notification_settings,
        name="customer_notification_settings",
    ),



    path(
        "customer-billing/settings/invoice-appearance/",
        views.customer_invoice_appearance,
        name="customer_invoice_appearance",
    ),


    path(
        "customer-billing/settings/bank-payment/",
        views.customer_bank_payment_settings,
        name="customer_bank_payment_settings",
    ),


    path(
        "customer-billing/settings/password/",
        views.customer_password_settings,
        name="customer_password_settings",
    ),


    path(
        "customer-billing/settings/security/",
        views.customer_security_settings,
        name="customer_security_settings",
    ),
    path(
        "logout_customer/",
        views.logout_customer,
        name="logout_customer"
    ),

    

]