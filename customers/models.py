from django.db import models
from app.models import Company
from django.contrib.auth.models import User


class Customer(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(
        max_length=200
    )

    sku = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    minimum_stock = models.PositiveIntegerField(
        default=0
    )

    supplier = models.CharField(
        max_length=200,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        default="Available"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CustomerInvoice(models.Model):

    STATUS_CHOICES = [
        ("Paid", "Paid"),
        ("Partial", "Partial"),
        ("Pending", "Pending"),
        ("Overdue", "Overdue"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_invoices"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="customer_invoices",
        null=True,
        blank=True
    )

    invoice_number = models.CharField(
        max_length=30
    )

    invoice_date = models.DateField()

    due_date = models.DateField()

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    gst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    balance_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-invoice_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "invoice_number"],
                name="unique_customer_invoice_number_per_company"
            )
        ]

    def __str__(self):
        return self.invoice_number


class CustomerPayment(models.Model):

    PAYMENT_METHODS = (
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Bank Transfer", "Bank Transfer"),
    )

    STATUS_CHOICES = (
        ("Paid", "Paid"),
        ("Partial", "Partial"),
        ("Pending", "Pending"),
        ("Failed", "Failed"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_payments"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    invoice = models.ForeignKey(
        CustomerInvoice,
        on_delete=models.CASCADE,
        related_name="payments",
        blank=True,
        null=True
    )

    receipt_number = models.CharField(
        max_length=30
    )

    payment_date = models.DateField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-payment_date"]
        verbose_name = "Customer Payment"
        verbose_name_plural = "Customer Payments"
        constraints = [
            models.UniqueConstraint(
                fields=["company", "receipt_number"],
                name="unique_customer_receipt_number_per_company"
            )
        ]

    def __str__(self):
        return f"{self.receipt_number} - {self.customer.name}"


class CustomerGSTSettings(models.Model):

    BUSINESS_TYPES = (
        ("Private Limited", "Private Limited"),
        ("Proprietorship", "Proprietorship"),
        ("Partnership", "Partnership"),
        ("LLP", "LLP"),
    )

    TAX_TYPES = (
        ("CGST + SGST", "CGST + SGST"),
        ("IGST", "IGST"),
    )

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_gst_settings"
    )

    company_name = models.CharField(
        max_length=150
    )

    gst_number = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    pan_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    business_type = models.CharField(
        max_length=100,
        choices=BUSINESS_TYPES,
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    state_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    cgst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=9.00
    )

    sgst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=9.00
    )

    igst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.00
    )

    default_tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPES,
        default="CGST + SGST"
    )

    contact_person = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Customer GST Setting"
        verbose_name_plural = "Customer GST Settings"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.company_name} ({self.gst_number or 'No GST'})"


class CustomerCompanyProfile(models.Model):

    COMPANY_TYPE_CHOICES = [
        ("business", "Business"),
        ("company", "Company"),
        ("startup", "Startup"),
        ("agency", "Agency"),
        ("education", "Education"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_company_profile"
    )

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    company_logo = models.ImageField(
        upload_to="customer_company_logos/",
        blank=True,
        null=True
    )

    company_type = models.CharField(
        max_length=50,
        choices=COMPANY_TYPE_CHOICES,
        default="company"
    )

    owner_name = models.CharField(
        max_length=150,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default="India",
        blank=True
    )

    pin_code = models.CharField(
        max_length=20,
        blank=True
    )

    gst_number = models.CharField(
        max_length=50,
        blank=True
    )

    pan_number = models.CharField(
        max_length=50,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company_name or self.user.username


class CustomerInvoiceSettings(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
        ("cheque", "Cheque"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_invoice_settings"
    )

    invoice_prefix = models.CharField(
        max_length=30,
        default="INV"
    )

    invoice_number_start = models.PositiveIntegerField(
        default=1
    )

    invoice_number_format = models.CharField(
        max_length=100,
        default="{prefix}-{year}-{number}"
    )

    auto_generate_invoice_number = models.BooleanField(
        default=True
    )

    default_due_days = models.PositiveIntegerField(
        default=0,
        help_text="Number of days after invoice date"
    )

    default_payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default="upi"
    )

    enable_gst = models.BooleanField(
        default=True
    )

    default_gst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18.00
    )

    currency = models.CharField(
        max_length=10,
        default="INR"
    )

    currency_symbol = models.CharField(
        max_length=10,
        default="₹"
    )

    show_company_logo = models.BooleanField(
        default=True
    )

    show_company_address = models.BooleanField(
        default=True
    )

    show_customer_gst = models.BooleanField(
        default=True
    )

    show_tax_breakdown = models.BooleanField(
        default=True
    )

    show_payment_details = models.BooleanField(
        default=True
    )

    show_signature = models.BooleanField(
        default=False
    )

    invoice_footer = models.TextField(
        blank=True,
        default="Thank you for your business."
    )

    invoice_terms = models.TextField(
        blank=True,
        default="Payment is due as per the invoice terms."
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Customer Invoice Setting"
        verbose_name_plural = "Customer Invoice Settings"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Invoice Settings - {self.company.company_name}"


class CustomerPaymentSettings(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("bank_transfer", "Bank Transfer"),
        ("upi", "UPI"),
        ("card", "Credit / Debit Card"),
        ("cheque", "Cheque"),
        ("online", "Online Payment"),
    ]

    PAYMENT_MODE_CHOICES = [
        ("manual", "Manual Payment"),
        ("online", "Online Payment"),
        ("both", "Manual + Online"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_payment_settings"
    )

    enable_payments = models.BooleanField(
        default=True
    )

    default_payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default="upi"
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        default="both"
    )

    default_due_days = models.PositiveIntegerField(
        default=0
    )

    allow_partial_payment = models.BooleanField(
        default=True
    )

    minimum_partial_payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    enable_online_payment = models.BooleanField(
        default=False
    )

    payment_gateway = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    payment_link_expiry_days = models.PositiveIntegerField(
        default=7
    )

    generate_receipt = models.BooleanField(
        default=True
    )

    receipt_prefix = models.CharField(
        max_length=20,
        default="REC"
    )

    receipt_number_start = models.PositiveIntegerField(
        default=1
    )

    send_payment_confirmation = models.BooleanField(
        default=True
    )

    send_payment_receipt = models.BooleanField(
        default=True
    )

    send_payment_reminder = models.BooleanField(
        default=True
    )

    mark_invoice_paid_automatically = models.BooleanField(
        default=True
    )

    allow_payment_edit = models.BooleanField(
        default=False
    )

    allow_payment_delete = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Payment Settings - {self.company}"


class CustomerTaxGSTSettings(models.Model):

    TAX_TYPE_CHOICES = [
        ("exclusive", "Tax Exclusive"),
        ("inclusive", "Tax Inclusive"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_tax_gst_settings"
    )

    enable_tax = models.BooleanField(
        default=True
    )

    enable_gst = models.BooleanField(
        default=True
    )

    gst_number = models.CharField(
        max_length=15,
        blank=True,
        default=""
    )

    gst_state_code = models.CharField(
        max_length=2,
        blank=True,
        default=""
    )

    tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPE_CHOICES,
        default="exclusive"
    )

    cgst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=9
    )

    sgst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=9
    )

    igst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=18
    )

    cess_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    apply_cgst_sgst = models.BooleanField(
        default=True
    )

    apply_igst = models.BooleanField(
        default=True
    )

    apply_cess = models.BooleanField(
        default=False
    )

    show_tax_on_invoice = models.BooleanField(
        default=True
    )

    show_gst_number_on_invoice = models.BooleanField(
        default=True
    )

    tax_rounding = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Tax & GST Settings - {self.company}"


class CustomerDiscountSettings(models.Model):

    DISCOUNT_TYPE_CHOICES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_discount_settings"
    )

    enable_discount = models.BooleanField(
        default=True
    )

    default_discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default="percentage"
    )

    default_discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    maximum_discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100
    )

    maximum_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    allow_invoice_discount = models.BooleanField(
        default=True
    )

    allow_item_discount = models.BooleanField(
        default=True
    )

    allow_manual_discount = models.BooleanField(
        default=True
    )

    require_discount_reason = models.BooleanField(
        default=False
    )

    apply_discount_before_tax = models.BooleanField(
        default=True
    )

    show_discount_on_invoice = models.BooleanField(
        default=True
    )

    show_discount_percentage = models.BooleanField(
        default=True
    )

    allow_discount_edit = models.BooleanField(
        default=True
    )

    allow_discount_delete = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Discount Settings - {self.company}"


class CustomerNotificationSettings(models.Model):

    REMINDER_FREQUENCY_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("before_due", "Before Due Date"),
        ("after_due", "After Due Date"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_notification_settings"
    )

    enable_notifications = models.BooleanField(
        default=True
    )

    enable_email_notifications = models.BooleanField(
        default=True
    )

    enable_sms_notifications = models.BooleanField(
        default=False
    )

    enable_whatsapp_notifications = models.BooleanField(
        default=False
    )

    send_invoice_notification = models.BooleanField(
        default=True
    )

    send_invoice_email = models.BooleanField(
        default=True
    )

    send_invoice_sms = models.BooleanField(
        default=False
    )

    send_invoice_whatsapp = models.BooleanField(
        default=False
    )

    send_payment_confirmation = models.BooleanField(
        default=True
    )

    send_payment_receipt = models.BooleanField(
        default=True
    )

    send_payment_email = models.BooleanField(
        default=True
    )

    send_payment_sms = models.BooleanField(
        default=False
    )

    send_payment_whatsapp = models.BooleanField(
        default=False
    )

    enable_payment_reminder = models.BooleanField(
        default=True
    )

    reminder_frequency = models.CharField(
        max_length=20,
        choices=REMINDER_FREQUENCY_CHOICES,
        default="before_due"
    )

    reminder_days_before_due = models.PositiveIntegerField(
        default=3
    )

    reminder_days_after_due = models.PositiveIntegerField(
        default=1
    )

    send_reminder_email = models.BooleanField(
        default=True
    )

    send_reminder_sms = models.BooleanField(
        default=False
    )

    send_reminder_whatsapp = models.BooleanField(
        default=False
    )

    send_overdue_notification = models.BooleanField(
        default=True
    )

    send_overdue_email = models.BooleanField(
        default=True
    )

    send_overdue_sms = models.BooleanField(
        default=False
    )

    send_overdue_whatsapp = models.BooleanField(
        default=False
    )

    send_customer_welcome = models.BooleanField(
        default=False
    )

    send_customer_account_update = models.BooleanField(
        default=False
    )

    notification_sender_name = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    notification_email = models.EmailField(
        blank=True,
        default=""
    )

    notification_phone = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Notification Settings - {self.company}"


class CustomerInvoiceAppearance(models.Model):

    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
    ]

    LAYOUT_CHOICES = [
        ("standard", "Standard"),
        ("modern", "Modern"),
        ("compact", "Compact"),
    ]

    LOGO_POSITION_CHOICES = [
        ("left", "Left"),
        ("center", "Center"),
        ("right", "Right"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_invoice_appearance"
    )

    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default="light"
    )

    accent_color = models.CharField(
        max_length=7,
        default="#2563eb"
    )

    layout = models.CharField(
        max_length=20,
        choices=LAYOUT_CHOICES,
        default="standard"
    )

    show_logo = models.BooleanField(
        default=True
    )

    logo = models.ImageField(
        upload_to="customer_invoice_logos/",
        blank=True,
        null=True
    )

    logo_position = models.CharField(
        max_length=20,
        choices=LOGO_POSITION_CHOICES,
        default="left"
    )

    show_company_name = models.BooleanField(
        default=True
    )

    show_company_address = models.BooleanField(
        default=True
    )

    show_company_phone = models.BooleanField(
        default=True
    )

    show_company_email = models.BooleanField(
        default=True
    )

    show_company_website = models.BooleanField(
        default=False
    )

    show_customer_address = models.BooleanField(
        default=True
    )

    show_customer_phone = models.BooleanField(
        default=True
    )

    show_customer_email = models.BooleanField(
        default=True
    )

    show_tax_details = models.BooleanField(
        default=True
    )

    show_payment_details = models.BooleanField(
        default=True
    )

    show_bank_details = models.BooleanField(
        default=False
    )

    show_footer = models.BooleanField(
        default=True
    )

    footer_text = models.CharField(
        max_length=500,
        blank=True,
        default="Thank you for your business."
    )

    terms_text = models.TextField(
        blank=True,
        default=""
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Customer Invoice Appearance"
        verbose_name_plural = "Customer Invoice Appearances"
        ordering = ["-updated_at"]

    def __str__(self):

        return (
            f"{self.company.company_name} - Invoice Appearance"
        )


class CustomerBankPaymentSettings(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("bank_transfer", "Bank Transfer"),
        ("upi", "UPI"),
        ("cash", "Cash"),
        ("card", "Card"),
        ("cheque", "Cheque"),
        ("online", "Online Payment"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_bank_payment_settings"
    )

    bank_name = models.CharField(
        max_length=150,
        blank=True
    )

    account_holder_name = models.CharField(
        max_length=150,
        blank=True
    )

    account_number = models.CharField(
        max_length=100,
        blank=True
    )

    ifsc_code = models.CharField(
        max_length=20,
        blank=True
    )

    branch_name = models.CharField(
        max_length=150,
        blank=True
    )

    account_type = models.CharField(
        max_length=50,
        blank=True
    )

    upi_id = models.CharField(
        max_length=100,
        blank=True
    )

    upi_name = models.CharField(
        max_length=150,
        blank=True
    )

    accept_bank_transfer = models.BooleanField(
        default=True
    )

    accept_upi = models.BooleanField(
        default=True
    )

    accept_cash = models.BooleanField(
        default=True
    )

    accept_card = models.BooleanField(
        default=False
    )

    accept_cheque = models.BooleanField(
        default=False
    )

    accept_online_payment = models.BooleanField(
        default=False
    )

    payment_instructions = models.TextField(
        blank=True,
        default=""
    )

    invoice_payment_note = models.TextField(
        blank=True,
        default=""
    )

    show_bank_details_on_invoice = models.BooleanField(
        default=True
    )

    show_upi_on_invoice = models.BooleanField(
        default=True
    )

    show_payment_instructions_on_invoice = models.BooleanField(
        default=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Customer Bank & Payment Setting"
        verbose_name_plural = "Customer Bank & Payment Settings"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Bank & Payment Settings - {self.company}"


class CustomerSecuritySettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="customer_security_settings"
    )

    require_strong_password = models.BooleanField(
        default=True
    )

    password_min_length = models.PositiveIntegerField(
        default=8
    )

    require_uppercase = models.BooleanField(
        default=True
    )

    require_lowercase = models.BooleanField(
        default=True
    )

    require_number = models.BooleanField(
        default=True
    )

    require_special_character = models.BooleanField(
        default=False
    )

    session_timeout_enabled = models.BooleanField(
        default=False
    )

    session_timeout_minutes = models.PositiveIntegerField(
        default=30
    )

    login_attempt_limit_enabled = models.BooleanField(
        default=True
    )

    max_login_attempts = models.PositiveIntegerField(
        default=5
    )

    two_factor_enabled = models.BooleanField(
        default=False
    )

    login_alerts = models.BooleanField(
        default=True
    )

    password_change_alerts = models.BooleanField(
        default=True
    )

    suspicious_login_alerts = models.BooleanField(
        default=True
    )

    allow_multiple_sessions = models.BooleanField(
        default=True
    )

    force_logout_after_password_change = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Security Settings - {self.company.company_name}"