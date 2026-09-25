from django.urls import path
from . import views

urlpatterns = [

    path("", views.billing_staff_login, name="billing_staff_login"),
    path("dashboard/", views.billing_dashboard, name="billing_dashboard"),
    path("create_invoice/", views.create_invoice, name="create_invoice"),
    path("create_invoice_list/", views.create_invoice_list, name="create_invoice_list"),
    path("invoice/<int:pk>/update/", views.create_invoice_update, name="create_invoice_update"),
    path("invoice/<int:pk>/delete/", views.create_invoice_delete, name="create_invoice_delete"),
    path("fee-configuration/", views.fee_configuration, name="fee_configuration"),
    path("fee-configuration/edit/<int:pk>/", views.edit_fee_configuration, name="edit_fee_configuration"),
    path("fee-configuration/delete/<int:pk>/", views.delete_fee_configuration,name="delete_fee_configuration"),
    path("gst-settings/", views.gst_settings, name="gst_settings"),
    path("gst-settings/edit/", views.edit_gst_settings, name="edit_gst_settings"),
    path("gst-settings/delete/", views.delete_gst_settings,name="delete_gst_settings"),
   path("billing_payment_list/", views.billing_payment_list, name="billing_payment_list"),
path("billing_payment_form/", views.billing_payment_form, name="billing_payment_form"),
path("payments/edit/<int:pk>/", views.edit_payment, name="edit_payment"),
path("payments/delete/<int:pk>/", views.delete_payment, name="delete_payment"),
    path("emi/", views.emi_list, name="emi_list"),
    path("emi/add/", views.emi_create, name="emi_create"),
    path("emi/<int:pk>/paid/", views.emi_paid, name="emi_paid"),
    path("emi/<int:pk>/edit/", views.emi_edit, name="emi_edit"),
    path("emi/<int:pk>/delete/", views.emi_delete, name="emi_delete"),
    path("invoice-report/", views.invoice_report, name="invoice_report"),
    path("billing_portal/", views.billing_portal,name="billing_portal"),
    path("billing-admin-login/",views.billing_admin_login,name="billing_admin_login"),
    path("billing_settings/", views.billing_settings, name="billing_settings"),
    path("billing_general_settings/", views.billing_general_settings, name="billing_general_settings"),
    path("billing_invoice_settings/", views.billing_invoice_settings, name="billing_invoice_settings"),
    path("billing_payment_settings/", views.billing_payment_settings, name="billing_payment_settings"),
    path("billing_tax_settings/", views.billing_tax_settings, name="billing_tax_settings"),
    path("billing_fee_settings/", views.billing_fee_settings, name="billing_fee_settings"),
    path("billing_late_fee_settings/", views.billing_late_fee_settings, name="billing_late_fee_settings"),
    path("billing_reminder_settings/", views.billing_reminder_settings, name="billing_reminder_settings"),
    path("billing_appearance_settings/", views.billing_appearance_settings, name="billing_appearance_settings"),
    path("billing_bank_settings/", views.billing_bank_settings, name="billing_bank_settings"),
  
     path(
        "logout/",
        views.logout_billing,
        name="logout_billing"
    ),
    path(
    "settings/company-profile/",
    views.billing_company_profile_settings,
    name="billing_company_profile_settings"
),


]