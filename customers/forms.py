from django import forms
from .models import CustomerCompanyProfile
from .models import CustomerInvoiceSettings
from .models import CustomerPaymentSettings
from .models import CustomerTaxGSTSettings
from .models import CustomerDiscountSettings
from .models import CustomerNotificationSettings
from .models import CustomerInvoiceAppearance
from .models import CustomerBankPaymentSettings
from .models import CustomerSecuritySettings



class CustomerCompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CustomerCompanyProfile

        fields = [
            "company_name",
            "company_logo",
            "company_type",
            "owner_name",
            "email",
            "phone",
            "website",
            "address",
            "city",
            "state",
            "country",
            "pin_code",
            "gst_number",
            "pan_number",
            "description",
        ]

        labels = {
            "company_name": "Company Name",
            "company_logo": "Company Logo",
            "company_type": "Company Type",
            "owner_name": "Owner / Manager Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "website": "Website",
            "address": "Business Address",
            "city": "City",
            "state": "State",
            "country": "Country",
            "pin_code": "PIN Code",
            "gst_number": "GST Number",
            "pan_number": "PAN Number",
            "description": "Company Description",
        }

        widgets = {
            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter company name",
                }
            ),

            "company_logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/png,image/jpeg,image/jpg",
                }
            ),

            "company_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "owner_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Owner / Manager Name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "company@example.com",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+91 9876543210",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter business address",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "State",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Country",
                }
            ),

            "pin_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "PIN Code",
                }
            ),

            "gst_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "22AAAAA0000A1Z5",
                }
            ),

            "pan_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ABCDE1234F",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe your company...",
                }
            ),
        }

    def clean_company_logo(self):
        logo = self.cleaned_data.get("company_logo")

        if logo:
            allowed_types = [
                "image/jpeg",
                "image/jpg",
                "image/png",
            ]

            if logo.content_type not in allowed_types:
                raise forms.ValidationError(
                    "Only PNG and JPG images are allowed."
                )

            if logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    "Logo size must be less than 2 MB."
                )

        return logo

class CustomerInvoiceSettingsForm(forms.ModelForm):

    class Meta:
        model = CustomerInvoiceSettings

        fields = [
            "invoice_prefix",
            "invoice_number_start",
            "invoice_number_format",
            "auto_generate_invoice_number",

            "default_due_days",
            "default_payment_method",

            "enable_gst",
            "default_gst_rate",

            "currency",
            "currency_symbol",

            "show_company_logo",
            "show_company_address",
            "show_customer_gst",
            "show_tax_breakdown",
            "show_payment_details",
            "show_signature",

            "invoice_footer",
            "invoice_terms",

            "is_active",
        ]

        widgets = {

            "invoice_prefix": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "INV",
                }
            ),

            "invoice_number_start": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                }
            ),

            "invoice_number_format": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "{prefix}-{year}-{number}",
                }
            ),

            "auto_generate_invoice_number": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "default_due_days": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "default_payment_method": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "enable_gst": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "default_gst_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "currency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "INR",
                }
            ),

            "currency_symbol": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "₹",
                }
            ),

            "show_company_logo": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "show_company_address": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "show_customer_gst": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "show_tax_breakdown": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "show_payment_details": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "show_signature": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "invoice_footer": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Thank you for your business.",
                }
            ),

            "invoice_terms": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Payment is due as per the invoice terms.",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),
        }




class CustomerPaymentSettingsForm(forms.ModelForm):

    class Meta:

        model = CustomerPaymentSettings

        fields = [
            # General
            "enable_payments",
            "default_payment_method",
            "payment_mode",

            # Due
            "default_due_days",
            "allow_partial_payment",
            "minimum_partial_payment",

            # Online
            "enable_online_payment",
            "payment_gateway",
            "payment_link_expiry_days",

            # Receipt
            "generate_receipt",
            "receipt_prefix",
            "receipt_number_start",

            # Notifications
            "send_payment_confirmation",
            "send_payment_receipt",
            "send_payment_reminder",

            # Status
            "mark_invoice_paid_automatically",
            "allow_payment_edit",
            "allow_payment_delete",
            "is_active",
        ]

        widgets = {

            "enable_payments": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "default_payment_method": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "default_due_days": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "placeholder": "0"
                }
            ),

            "allow_partial_payment": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "minimum_partial_payment": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "0.00"
                }
            ),

            "enable_online_payment": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "payment_gateway": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Razorpay / Stripe / PayU"
                }
            ),

            "payment_link_expiry_days": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "7"
                }
            ),

            "generate_receipt": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "receipt_prefix": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "REC"
                }
            ),

            "receipt_number_start": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "1"
                }
            ),

            "send_payment_confirmation": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "send_payment_receipt": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "send_payment_reminder": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "mark_invoice_paid_automatically": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "allow_payment_edit": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "allow_payment_delete": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if not isinstance(
                field.widget,
                forms.CheckboxInput
            ):
                field.widget.attrs.setdefault(
                    "class",
                    "form-control"
                )



class CustomerTaxGSTSettingsForm(forms.ModelForm):

    class Meta:
        model = CustomerTaxGSTSettings

        fields = [
            "enable_tax",
            "enable_gst",
            "gst_number",
            "gst_state_code",
            "tax_type",
            "cgst_rate",
            "sgst_rate",
            "igst_rate",
            "cess_rate",
            "apply_cgst_sgst",
            "apply_igst",
            "apply_cess",
            "show_tax_on_invoice",
            "show_gst_number_on_invoice",
            "tax_rounding",
            "is_active",
        ]

        widgets = {

            "enable_tax": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),

            "enable_gst": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),

            "gst_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter GSTIN"
                }
            ),

            "gst_state_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter state code",
                    "maxlength": "2"
                }
            ),

            "tax_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "cgst_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "sgst_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "igst_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "cess_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "apply_cgst_sgst": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),

            "apply_igst": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),

            "apply_cess": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),

            "show_tax_on_invoice": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),

            "show_gst_number_on_invoice": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),

            "tax_rounding": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),

            "is_active": forms.CheckboxInput(
                attrs={"class": "toggle-input"}
            ),
        }

    def clean_gst_number(self):
        gst_number = self.cleaned_data.get("gst_number", "").strip().upper()

        if gst_number and len(gst_number) != 15:
            raise forms.ValidationError(
                "GSTIN must contain exactly 15 characters."
            )

        return gst_number

    def clean_gst_state_code(self):
        return self.cleaned_data.get(
            "gst_state_code",
            ""
        ).strip()



class CustomerDiscountSettingsForm(forms.ModelForm):

    class Meta:

        model = CustomerDiscountSettings

        fields = [
            "enable_discount",
            "default_discount_type",
            "default_discount_value",
            "maximum_discount_percentage",
            "maximum_discount_amount",
            "allow_invoice_discount",
            "allow_item_discount",
            "allow_manual_discount",
            "require_discount_reason",
            "apply_discount_before_tax",
            "show_discount_on_invoice",
            "show_discount_percentage",
            "allow_discount_edit",
            "allow_discount_delete",
            "is_active",
        ]

        widgets = {

            "enable_discount": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "default_discount_type": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "default_discount_value": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "maximum_discount_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "max": "100"
                }
            ),

            "maximum_discount_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "allow_invoice_discount": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "allow_item_discount": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "allow_manual_discount": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "require_discount_reason": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "apply_discount_before_tax": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "show_discount_on_invoice": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "show_discount_percentage": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "allow_discount_edit": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "allow_discount_delete": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input"
                }
            ),
        }



class CustomerNotificationSettingsForm(forms.ModelForm):

    class Meta:

        model = CustomerNotificationSettings

        fields = [
            "enable_notifications",

            "enable_email_notifications",
            "enable_sms_notifications",
            "enable_whatsapp_notifications",

            "send_invoice_notification",
            "send_invoice_email",
            "send_invoice_sms",
            "send_invoice_whatsapp",

            "send_payment_confirmation",
            "send_payment_receipt",
            "send_payment_email",
            "send_payment_sms",
            "send_payment_whatsapp",

            "enable_payment_reminder",
            "reminder_frequency",
            "reminder_days_before_due",
            "reminder_days_after_due",

            "send_reminder_email",
            "send_reminder_sms",
            "send_reminder_whatsapp",

            "send_overdue_notification",
            "send_overdue_email",
            "send_overdue_sms",
            "send_overdue_whatsapp",

            "send_customer_welcome",
            "send_customer_account_update",

            "notification_sender_name",
            "notification_email",
            "notification_phone",

            "is_active",
        ]

        widgets = {

            "enable_notifications":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "enable_email_notifications":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "enable_sms_notifications":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "enable_whatsapp_notifications":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_invoice_notification":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_invoice_email":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_invoice_sms":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_invoice_whatsapp":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_payment_confirmation":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_payment_receipt":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_payment_email":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_payment_sms":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_payment_whatsapp":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "enable_payment_reminder":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "reminder_frequency":
                forms.Select(
                    attrs={"class": "form-control"}
                ),

            "reminder_days_before_due":
                forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "min": "0"
                    }
                ),

            "reminder_days_after_due":
                forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "min": "0"
                    }
                ),

            "send_reminder_email":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_reminder_sms":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_reminder_whatsapp":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_overdue_notification":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_overdue_email":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_overdue_sms":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_overdue_whatsapp":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_customer_welcome":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "send_customer_account_update":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),

            "notification_sender_name":
                forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "FlowTenant"
                    }
                ),

            "notification_email":
                forms.EmailInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "billing@example.com"
                    }
                ),

            "notification_phone":
                forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "+91 9876543210"
                    }
                ),

            "is_active":
                forms.CheckboxInput(
                    attrs={"class": "toggle-input"}
                ),
        }


class CustomerInvoiceAppearanceForm(forms.ModelForm):

    class Meta:
        model = CustomerInvoiceAppearance

        fields = [
            "theme",
            "accent_color",
            "layout",

            "show_logo",
            "logo",
            "logo_position",

            "show_company_name",
            "show_company_address",
            "show_company_phone",
            "show_company_email",
            "show_company_website",

            "show_customer_address",
            "show_customer_phone",
            "show_customer_email",

            "show_tax_details",
            "show_payment_details",
            "show_bank_details",

            "show_footer",
            "footer_text",
            "terms_text",

            "is_active",
        ]

        widgets = {

            "theme": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "accent_color": forms.TextInput(
                attrs={
                    "class": "form-control color-input",
                    "type": "color",
                }
            ),

            "layout": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "show_logo": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "logo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "logo_position": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "show_company_name": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_company_address": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_company_phone": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_company_email": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_company_website": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_customer_address": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_customer_phone": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_customer_email": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_tax_details": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_payment_details": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_bank_details": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "show_footer": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),

            "footer_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Thank you for your business.",
                }
            ),

            "terms_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter invoice terms and conditions...",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "toggle-input",
                }
            ),
        }
class CustomerBankPaymentSettingsForm(forms.ModelForm):

    class Meta:

        model = CustomerBankPaymentSettings

        fields = [
            # Bank
            "bank_name",
            "account_holder_name",
            "account_number",
            "ifsc_code",
            "branch_name",
            "account_type",

            # UPI
            "upi_id",
            "upi_name",

            # Payment methods
            "accept_bank_transfer",
            "accept_upi",
            "accept_cash",
            "accept_card",
            "accept_cheque",
            "accept_online_payment",

            # Instructions
            "payment_instructions",
            "invoice_payment_note",

            # Display
            "show_bank_details_on_invoice",
            "show_upi_on_invoice",
            "show_payment_instructions_on_invoice",

            "is_active",
        ]

        widgets = {

            "bank_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter bank name",
                }
            ),

            "account_holder_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter account holder name",
                }
            ),

            "account_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter account number",
                }
            ),

            "ifsc_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: SBIN0001234",
                    "style": "text-transform: uppercase;",
                }
            ),

            "branch_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter branch name",
                }
            ),

            "account_type": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Current / Savings",
                }
            ),

            "upi_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@upi",
                }
            ),

            "upi_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "UPI account name",
                }
            ),

            "payment_instructions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Enter payment instructions for customers..."
                    ),
                }
            ),

            "invoice_payment_note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Enter the payment note shown on invoices..."
                    ),
                }
            ),
        }



class CustomerSecuritySettingsForm(forms.ModelForm):

    class Meta:

        model = CustomerSecuritySettings

        fields = [
            "require_strong_password",
            "password_min_length",
            "require_uppercase",
            "require_lowercase",
            "require_number",
            "require_special_character",

            "session_timeout_enabled",
            "session_timeout_minutes",

            "login_attempt_limit_enabled",
            "max_login_attempts",

            "two_factor_enabled",

            "login_alerts",
            "password_change_alerts",
            "suspicious_login_alerts",

            "allow_multiple_sessions",
            "force_logout_after_password_change",

            "is_active",
        ]

        widgets = {

            "password_min_length": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "6",
                    "max": "32",
                }
            ),

            "session_timeout_minutes": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "5",
                    "max": "1440",
                }
            ),

            "max_login_attempts": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "max": "20",
                }
            ),
        }

    def clean_password_min_length(self):

        value = self.cleaned_data["password_min_length"]

        if value < 6:
            raise forms.ValidationError(
                "Password length must be at least 6 characters."
            )

        if value > 32:
            raise forms.ValidationError(
                "Password length cannot exceed 32 characters."
            )

        return value

    def clean_session_timeout_minutes(self):

        value = self.cleaned_data["session_timeout_minutes"]

        if value < 5:
            raise forms.ValidationError(
                "Session timeout must be at least 5 minutes."
            )

        return value

    def clean_max_login_attempts(self):

        value = self.cleaned_data["max_login_attempts"]

        if value < 1:
            raise forms.ValidationError(
                "Login attempts must be at least 1."
            )

        return value