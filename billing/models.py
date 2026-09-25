from decimal import Decimal

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models
from django.utils import timezone

from app.models import Company
from students.models import Student

MONEY_VALIDATOR = MinValueValidator(
    Decimal("0.00")
)



class Invoice(models.Model):

    PAYMENT_CHOICES = [
        ("Full", "Full Payment"),
        ("Partial", "Partial Payment"),
        ("Split", "Split Payment"),
        ("EMI", "EMI"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Partial", "Partial"),
        ("Paid", "Paid"),
        ("Overdue", "Overdue"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    invoice_number = models.CharField(
        max_length=30,
        blank=True
    )

    # ADD THIS FIELD
    invoice_date = models.DateField(
        default=timezone.localdate
    )

    course_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MONEY_VALIDATOR]
    )

    registration_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MONEY_VALIDATOR]
    )

    gst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MONEY_VALIDATOR]
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MONEY_VALIDATOR]
    )

    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MONEY_VALIDATOR]
    )

    balance_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MONEY_VALIDATOR]
    )

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="Full"
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-invoice_date", "-id"]

    def save(self, *args, **kwargs):

        if not self.invoice_number:
            last = Invoice.objects.filter(
                company=self.company
            ).order_by("-id").first()

            next_no = 1 if not last else last.id + 1
            self.invoice_number = f"INV-{next_no:05d}"

        self.balance_amount = max(
            Decimal("0.00"),
            self.total_amount - self.amount_paid
        )

        today = timezone.localdate()

        if self.balance_amount == 0:
            self.status = "Paid"
        elif self.due_date and self.due_date < today:
            self.status = "Overdue"
        elif self.amount_paid > 0:
            self.status = "Partial"
        else:
            self.status = "Pending"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

class FeeConfiguration(models.Model):

    FEE_CHOICES = (
        ("Admission Fee", "Admission Fee"),
        ("Tuition Fee", "Tuition Fee"),
        ("Exam Fee", "Exam Fee"),
        ("Library Fee", "Library Fee"),
        ("Transport Fee", "Transport Fee"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="fee_configurations",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="fee_configurations",
        blank=True,
        null=True,
    )

    course = models.CharField(
        max_length=100,
        blank=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    fee_type = models.CharField(
        max_length=100,
        choices=FEE_CHOICES,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MONEY_VALIDATOR],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at", "-id"]

        indexes = [
            models.Index(
                fields=["company", "fee_type"],
            ),
            models.Index(
                fields=["company", "course"],
            ),
        ]

    def __str__(self):

        if self.student:
            return (
                f"{self.student.first_name} "
                f"{self.student.last_name} - "
                f"{self.fee_type}"
            )

        return f"{self.course} - {self.fee_type}"


class GSTSettings(models.Model):

    TAX_MODE_CHOICES = [
        ("exclusive", "Tax Exclusive"),
        ("inclusive", "Tax Inclusive"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="gst_settings",
    )


    is_active = models.BooleanField(
        default=True
    )

    gst_number = models.CharField(
        max_length=15,
        blank=True,
    )

    default_gst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("18.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(100),
        ],
    )

    tax_mode = models.CharField(
        max_length=20,
        choices=TAX_MODE_CHOICES,
        default="exclusive",
    )

    cgst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("9.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(100),
        ],
    )

    sgst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("9.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(100),
        ],
    )

    igst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("18.00"),
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(100),
        ],
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    place_of_supply = models.CharField(
        max_length=100,
        blank=True,
    )

    hsn_sac_code = models.CharField(
        max_length=30,
        blank=True,
    )

    apply_gst_automatically = models.BooleanField(
        default=True
    )

    show_gst_on_invoice = models.BooleanField(
        default=True
    )

    tax_inclusive_pricing = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.company.company_name} - Tax & GST Settings"

class Payment(models.Model):

    PAYMENT_METHODS = (
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Bank", "Bank Transfer"),
        ("Cheque", "Cheque"),
    )

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Partial", "Partial"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="billing_payments",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="billing_payments",
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        related_name="payments",
        blank=True,
        null=True,
    )

    course = models.CharField(
        max_length=100,
        blank=True,
    )

    receipt_number = models.CharField(
        max_length=30,
        blank=True,
        db_index=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MONEY_VALIDATOR],
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHODS,
        default="Cash",
    )

    payment_date = models.DateField(
        default=timezone.now,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Paid",
    )

    remarks = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-payment_date", "-id"]

        constraints = [
            models.UniqueConstraint(
                fields=["company", "receipt_number"],
                name="unique_receipt_number_per_company",
            ),
        ]

        indexes = [
            models.Index(
                fields=["company", "payment_date"],
            ),
            models.Index(
                fields=["company", "status"],
            ),
        ]

    def save(self, *args, **kwargs):

        if not self.receipt_number:

            last_payment = (
                Payment.objects
                .filter(company=self.company)
                .order_by("-id")
                .first()
            )

            next_number = (
                last_payment.id + 1
                if last_payment
                else 1
            )

            self.receipt_number = (
                f"PAY-{next_number:05d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.receipt_number

class EMI(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Overdue", "Overdue"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="emis",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="emis",
    )

    installment_no = models.PositiveIntegerField()

    due_date = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MONEY_VALIDATOR],
    )

    paid_date = models.DateField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["due_date", "installment_no"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "student",
                    "installment_no",
                ],
                name="unique_student_emi_installment",
            ),
        ]

        indexes = [
            models.Index(
                fields=["company", "status"],
            ),
            models.Index(
                fields=["company", "due_date"],
            ),
        ]

    def save(self, *args, **kwargs):

        today = timezone.now().date()

        if self.status != "Paid":

            if self.due_date < today:
                self.status = "Overdue"
            else:
                self.status = "Pending"

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.student.first_name} "
            f"- EMI {self.installment_no}"
        )

class BillingSettings(models.Model):

    CURRENCY_CHOICES = [
        ("INR", "Indian Rupee (INR)"),
        ("USD", "US Dollar (USD)"),
        ("EUR", "Euro (EUR)"),
        ("GBP", "British Pound (GBP)"),
    ]

    FINANCIAL_YEAR_CHOICES = [
        ("april_march", "April - March"),
        ("january_december", "January - December"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("bank", "Bank Transfer"),
        ("upi", "UPI"),
        ("card", "Card"),
        ("cheque", "Cheque"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="billing_settings",
    )

    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default="INR",
    )

    currency_symbol = models.CharField(
        max_length=5,
        default="₹",
    )


    financial_year = models.CharField(
        max_length=30,
        choices=FINANCIAL_YEAR_CHOICES,
        default="april_march",
    )

    payment_terms = models.PositiveIntegerField(
        default=30,
        validators=[
            MinValueValidator(0),
        ],
    )


    billing_enabled = models.BooleanField(
        default=True,
    )

    allow_partial_payment = models.BooleanField(
        default=True,
    )

    auto_payment_status = models.BooleanField(
        default=True,
    )

    payment_receipt = models.BooleanField(
        default=True,
    )

    auto_invoice_generation = models.BooleanField(
        default=False,
    )


    default_payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cash",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Billing Settings"
        verbose_name_plural = "Billing Settings"

    def __str__(self):
        return (
            f"{self.company.company_name} - "
            f"Billing Settings"
        )


class InvoiceSettings(models.Model):

    FORMAT_CHOICES = [
        ("PREFIX-NUMBER", "INV-00001"),
        ("PREFIX-YEAR-NUMBER", "INV-2026-00001"),
        ("YEAR-PREFIX-NUMBER", "2026-INV-00001"),
    ]

    DATE_TYPE_CHOICES = [
        ("today", "Current Date"),
        ("creation", "Creation Date"),
    ]

    DUE_DATE_CHOICES = [
        ("payment_terms", "Based on Payment Terms"),
        ("manual", "Enter Manually"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="invoice_settings",
    )

    invoice_prefix = models.CharField(
        max_length=20,
        default="INV",
    )

    invoice_format = models.CharField(
        max_length=30,
        choices=FORMAT_CHOICES,
        default="PREFIX-YEAR-NUMBER",
    )

    starting_number = models.PositiveIntegerField(
        default=1,
    )

    number_digits = models.PositiveIntegerField(
        default=5,
    )

    automatic_numbering = models.BooleanField(
        default=True,
    )

    invoice_date_type = models.CharField(
        max_length=20,
        choices=DATE_TYPE_CHOICES,
        default="today",
    )

    due_date_mode = models.CharField(
        max_length=30,
        choices=DUE_DATE_CHOICES,
        default="payment_terms",
    )

    show_student_details = models.BooleanField(
        default=True,
    )

    show_course_details = models.BooleanField(
        default=True,
    )

    show_fee_breakdown = models.BooleanField(
        default=True,
    )

    show_gst_breakdown = models.BooleanField(
        default=True,
    )

    show_payment_status = models.BooleanField(
        default=True,
    )

    show_balance_due = models.BooleanField(
        default=True,
    )

    auto_total_calculation = models.BooleanField(
        default=True,
    )

    auto_balance_calculation = models.BooleanField(
        default=True,
    )

    auto_pdf_generation = models.BooleanField(
        default=False,
    )

    allow_duplicate_invoice = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.company} - Invoice Settings"

class PaymentSettings(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("upi", "UPI"),
        ("bank", "Bank Transfer"),
        ("card", "Card"),
        ("cheque", "Cheque"),
    ]

    RECEIPT_FORMAT_CHOICES = [
        ("PREFIX-NUMBER", "PAY-00001"),
        ("PREFIX-YEAR-NUMBER", "PAY-2026-00001"),
        ("YEAR-PREFIX-NUMBER", "2026-PAY-00001"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="payment_settings",
    )

    cash_enabled = models.BooleanField(default=True)

    upi_enabled = models.BooleanField(default=True)

    bank_enabled = models.BooleanField(default=True)

    card_enabled = models.BooleanField(default=False)

    cheque_enabled = models.BooleanField(default=False)

    default_payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="upi",
    )

    allow_partial_payment = models.BooleanField(
        default=True
    )

    require_reference = models.BooleanField(
        default=False
    )

    automatic_payment_status = models.BooleanField(
        default=True
    )

    generate_receipt = models.BooleanField(
        default=True
    )

    receipt_prefix = models.CharField(
        max_length=20,
        default="PAY"
    )

    receipt_digits = models.PositiveIntegerField(
        default=5
    )

    receipt_format = models.CharField(
        max_length=30,
        choices=RECEIPT_FORMAT_CHOICES,
        default="PREFIX-NUMBER",
    )

    receipt_starting_number = models.PositiveIntegerField(
        default=1
    )

    online_payment_enabled = models.BooleanField(
        default=False
    )

    payment_confirmation = models.BooleanField(
        default=True
    )

    payment_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.company.company_name} - Payment Settings"




class FeeDiscountSettings(models.Model):

    FEE_TYPE_CHOICES = [
        ("Admission Fee", "Admission Fee"),
        ("Tuition Fee", "Tuition Fee"),
        ("Exam Fee", "Exam Fee"),
        ("Library Fee", "Library Fee"),
        ("Transport Fee", "Transport Fee"),
        ("Other", "Other"),
    ]

    DISCOUNT_TYPE_CHOICES = [
        ("percentage", "Percentage (%)"),
        ("fixed", "Fixed Amount"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="fee_discount_settings",
    )


    fee_system_enabled = models.BooleanField(
        default=True
    )

    default_fee_type = models.CharField(
        max_length=50,
        choices=FEE_TYPE_CHOICES,
        default="Tuition Fee",
    )

    allow_custom_fees = models.BooleanField(
        default=True
    )

    allow_discounts = models.BooleanField(
        default=True
    )

    default_discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default="percentage",
    )

    default_discount_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(
                Decimal("0.00")
            )
        ],
    )

    maximum_discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("100.00"),
        validators=[
            MinValueValidator(
                Decimal("0.00")
            )
        ],
    )

    apply_discount_before_tax = models.BooleanField(
        default=True
    )

    round_fee_amounts = models.BooleanField(
        default=False
    )

    show_discount_on_invoice = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.company.company_name} - "
            f"Fee & Discount Settings"
        )



class LateFeeSettings(models.Model):

    LATE_FEE_TYPE_CHOICES = [
        ("percentage", "Percentage (%)"),
        ("fixed", "Fixed Amount"),
    ]

    REPEAT_INTERVAL_CHOICES = [
        ("once", "One Time"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="late_fee_settings",
    )

    enabled = models.BooleanField(
        default=False
    )


    grace_period_days = models.PositiveIntegerField(
        default=0
    )

    late_fee_type = models.CharField(
        max_length=20,
        choices=LATE_FEE_TYPE_CHOICES,
        default="percentage",
    )

    late_fee_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(
                Decimal("0.00")
            )
        ],
    )

    maximum_late_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(
                Decimal("0.00")
            )
        ],
    )


    apply_automatically = models.BooleanField(
        default=True
    )

    apply_on_overdue = models.BooleanField(
        default=True
    )

    repeat_late_fee = models.BooleanField(
        default=False
    )

    repeat_interval = models.CharField(
        max_length=20,
        choices=REPEAT_INTERVAL_CHOICES,
        default="monthly",
    )

    show_on_invoice = models.BooleanField(
        default=True
    )

    late_fee_description = models.CharField(
        max_length=255,
        default="Late payment fee",
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.company.company_name} - "
            f"Late Fee Settings"
        )



class PaymentReminderSettings(models.Model):

    REPEAT_INTERVAL_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="payment_reminder_settings",
    )


    enabled = models.BooleanField(
        default=True
    )
    reminder_before_due = models.BooleanField(
        default=True
    )

    before_due_days = models.PositiveIntegerField(
        default=3
    )

    reminder_on_due_date = models.BooleanField(
        default=True
    )


    reminder_after_due = models.BooleanField(
        default=True
    )

    after_due_days = models.PositiveIntegerField(
        default=1
    )

    repeat_reminders = models.BooleanField(
        default=False
    )

    repeat_interval = models.CharField(
        max_length=20,
        choices=REPEAT_INTERVAL_CHOICES,
        default="weekly",
    )

    maximum_reminders = models.PositiveIntegerField(
        default=3
    )

    email_reminders = models.BooleanField(
        default=True
    )

    sms_reminders = models.BooleanField(
        default=False
    )

    whatsapp_reminders = models.BooleanField(
        default=False
    )

    show_invoice_number = models.BooleanField(
        default=True
    )

    show_due_amount = models.BooleanField(
        default=True
    )

    show_due_date = models.BooleanField(
        default=True
    )

    reminder_message = models.TextField(
        blank=True,
        default=(
            "Dear Customer, your payment is pending. "
            "Please complete the payment before the due date."
        ),
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.company.company_name} - "
            f"Payment Reminder Settings"
        )

class BillingAppearanceSettings(models.Model):

    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
    ]

    FONT_SIZE_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    INVOICE_LAYOUT_CHOICES = [
        ("standard", "Standard"),
        ("modern", "Modern"),
        ("compact", "Compact"),
    ]

    LOGO_POSITION_CHOICES = [
        ("left", "Left"),
        ("center", "Center"),
        ("right", "Right"),
    ]

    DATE_FORMAT_CHOICES = [
        ("DD/MM/YYYY", "DD/MM/YYYY"),
        ("MM/DD/YYYY", "MM/DD/YYYY"),
        ("YYYY-MM-DD", "YYYY-MM-DD"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="billing_appearance_settings",
    )
    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default="light",
    )

    primary_color = models.CharField(
        max_length=7,
        default="#2563EB",
    )

    accent_color = models.CharField(
        max_length=7,
        default="#3B1C35",
    )

    table_header_background = models.CharField(
        max_length=7,
        default="#3B1C35",
    )

    table_header_text_color = models.CharField(
        max_length=7,
        default="#FFFFFF",
    )


    font_family = models.CharField(
        max_length=50,
        default="Arial",
    )

    font_size = models.CharField(
        max_length=20,
        choices=FONT_SIZE_CHOICES,
        default="medium",
    )

    invoice_layout = models.CharField(
        max_length=20,
        choices=INVOICE_LAYOUT_CHOICES,
        default="standard",
    )

    logo_position = models.CharField(
        max_length=20,
        choices=LOGO_POSITION_CHOICES,
        default="left",
    )

    invoice_title = models.CharField(
        max_length=100,
        default="INVOICE",
    )

    date_format = models.CharField(
        max_length=20,
        choices=DATE_FORMAT_CHOICES,
        default="DD/MM/YYYY",
    )

    show_company_logo = models.BooleanField(
        default=True,
    )

    show_company_details = models.BooleanField(
        default=True,
    )

    show_customer_details = models.BooleanField(
        default=True,
    )

    show_payment_details = models.BooleanField(
        default=True,
    )

    show_tax_details = models.BooleanField(
        default=True,
    )

    show_signature = models.BooleanField(
        default=True,
    )

    show_qr_code = models.BooleanField(
        default=False,
    )

    show_invoice_footer = models.BooleanField(
        default=True,
    )


    show_watermark = models.BooleanField(
        default=False,
    )

    watermark_text = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    watermark_opacity = models.PositiveIntegerField(
        default=10,
    )

    custom_footer_text = models.TextField(
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        verbose_name = "Billing Appearance Settings"

        verbose_name_plural = (
            "Billing Appearance Settings"
        )

    def __str__(self):

        return (
            f"Billing Appearance - "
            f"{self.company.company_name}"
        )

class BankPaymentSettings(models.Model):

    ACCOUNT_TYPE_CHOICES = [
        ("savings", "Savings Account"),
        ("current", "Current Account"),
        ("cash_credit", "Cash Credit"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="bank_payment_settings",
    )

    bank_name = models.CharField(
        max_length=150,
        blank=True,
    )

    account_holder_name = models.CharField(
        max_length=150,
        blank=True,
    )

    account_number = models.CharField(
        max_length=50,
        blank=True,
    )

    account_type = models.CharField(
        max_length=30,
        choices=ACCOUNT_TYPE_CHOICES,
        default="current",
    )

    ifsc_code = models.CharField(
        max_length=20,
        blank=True,
    )

    branch_name = models.CharField(
        max_length=150,
        blank=True,
    )

    bank_address = models.TextField(
        blank=True,
    )

    upi_enabled = models.BooleanField(
        default=True,
    )

    upi_id = models.CharField(
        max_length=150,
        blank=True,
    )

    upi_name = models.CharField(
        max_length=150,
        blank=True,
    )

    show_bank_details = models.BooleanField(
        default=True,
    )

    show_upi_details = models.BooleanField(
        default=True,
    )

    show_on_invoice = models.BooleanField(
        default=True,
    )

    payment_instructions = models.TextField(
        blank=True,
        default=(
            "Please mention the invoice number while making "
            "a bank or UPI payment."
        ),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return (
            f"{self.company.company_name} - "
            f"Bank & Payment"
        )


class BillingCompanyProfile(models.Model):
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="billing_profile"
    )

    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=20, blank=True)

    gst_number = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Billing Company Profile"
        verbose_name_plural = "Billing Company Profiles"

    def __str__(self):
        return self.company_name or self.company.company_name