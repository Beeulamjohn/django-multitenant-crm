from django import forms
from django.db import models
from django.contrib.auth.models import User
from app.models import Company
from django.db.models import Max
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Completed", "Completed"),
        ("Dropped", "Dropped"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="students",
    )

    student_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Student ID",
    )

    admission_number = models.CharField(
        max_length=100,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    dob = models.DateField(
        blank=True,
        null=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )

    photo = models.ImageField(
        upload_to="students/photos/",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
    )

    mobile = models.CharField(
        max_length=20,
    )

    father_name = models.CharField(
        max_length=255,
        blank=True,
    )

    mother_name = models.CharField(
        max_length=255,
        blank=True,
    )

    parent_mobile = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="India",
    )

    pincode = models.CharField(
        max_length=20,
        blank=True,
    )

    course = models.CharField(
        max_length=200,
    )

    department = models.CharField(
        max_length=200,
        blank=True,
    )

    batch = models.CharField(
        max_length=100,
        blank=True,
    )

    semester = models.CharField(
        max_length=50,
        blank=True,
    )

    roll_number = models.CharField(
        max_length=100,
        blank=True,
    )

    admission_date = models.DateField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active",
    )

    aadhaar = models.FileField(
        upload_to="students/aadhaar/",
        blank=True,
        null=True,
    )

    marksheet = models.FileField(
        upload_to="students/marksheets/",
        blank=True,
        null=True,
    )

    transfer_certificate = models.FileField(
        upload_to="students/tc/",
        blank=True,
        null=True,
    )

    birth_certificate = models.FileField(
        upload_to="students/birth/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ("company", "admission_number")
        ordering = ["-created_at"]
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_id = (
                Student.objects.aggregate(Max("id"))["id__max"] or 0
            )
            self.student_id = f"STU{last_id + 1:05d}"

        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"


class StudentDocument(models.Model):
    DOCUMENT_TYPES = (
        ("Aadhaar", "Aadhaar"),
        ("SSLC", "SSLC"),
        ("PlusTwo", "Plus Two"),
        ("Degree", "Degree"),
        ("Transfer", "Transfer Certificate"),
        ("Conduct", "Conduct Certificate"),
        ("Resume", "Resume"),
        ("Other", "Other"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=100,
        choices=DOCUMENT_TYPES,
    )

    file = models.FileField(
        upload_to="students/documents/",
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Student Document"
        verbose_name_plural = "Student Documents"

    def __str__(self):
        return f"{self.student.full_name} - {self.document_type}"



class Course(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="courses",
    )

    course_code = models.CharField(
        max_length=20,
    )

    course_name = models.CharField(
        max_length=200,
    )

    duration = models.CharField(
        max_length=100,
    )

    fees = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ("company", "course_code")
        ordering = ["course_name"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"



class StudentStaff(models.Model):
    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Resigned", "Resigned"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="student_staffs",
    )

    staff_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15,
    )

    address = models.TextField(
        blank=True,
        null=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    joining_date = models.DateField(
        blank=True,
        null=True,
    )

    qualification = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    certification = models.FileField(
        upload_to="staff/certificates/",
        blank=True,
        null=True,
    )

    profile = models.ImageField(
        upload_to="staff/profile/",
        blank=True,
        null=True,
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ("company", "staff_id")
        ordering = ["first_name"]
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            last = StudentStaff.objects.aggregate(Max("id"))["id__max"] or 0
            self.staff_id = f"STF{last + 1:05d}"

        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.staff_id} - {self.full_name}"

class CompanyProfile(models.Model):

    COMPANY_TYPES = (
        ("education", "Education"),
        ("billing", "Billing"),
    )

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    company_name = models.CharField(
        max_length=200
    )

    company_logo = models.ImageField(
        upload_to="company/logo/",
        blank=True,
        null=True
    )

    company_type = models.CharField(
        max_length=20,
        choices=COMPANY_TYPES,
        default="education"
    )

    owner_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    website = models.URLField(
        blank=True
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    pin_code = models.CharField(
        max_length=20
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

    class Meta:
        ordering = ["company_name"]

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):

    ROLE_CHOICES = (
        ("admin", "Administrator"),
        ("staff", "Staff"),
        ("manager", "Manager"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    full_name = models.CharField(
        max_length=150,
        blank=True
    )

    mobile_number = models.CharField(
        max_length=20,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="staff"
    )

    two_factor_enabled = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.username
class LoginHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="login_history",
    )

    login_time = models.DateTimeField(
        auto_now_add=True,
    )

    logout_time = models.DateTimeField(
        blank=True,
        null=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    browser = models.CharField(
        max_length=100,
        blank=True,
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True,
    )

    device = models.CharField(
        max_length=150,
        blank=True,
    )

    successful = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["-login_time"]
        verbose_name = "Login History"
        verbose_name_plural = "Login History"

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.login_time:%d-%m-%Y %H:%M}"
        )


class ActiveDevice(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="active_devices",
    )

    device_name = models.CharField(
        max_length=150,
    )

    browser = models.CharField(
        max_length=100,
        blank=True,
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    session_key = models.CharField(
        max_length=100,
        unique=True,
    )

    is_current = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    last_activity = models.DateTimeField(
        auto_now=True,
    )

    login_time = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-last_activity"]
        verbose_name = "Active Device"
        verbose_name_plural = "Active Devices"

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.device_name}"
        )


class UserSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_sessions"
    )

    session_key = models.CharField(
        max_length=255,
        unique=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    device_name = models.CharField(
        max_length=100,
        default="Desktop"
    )

    browser = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    operating_system = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    last_activity = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.device_name}"


class EmployeeSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_settings",
    )

    working_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=8.0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(24),
        ],
    )

    office_start = models.TimeField(
        default="09:00",
    )

    office_end = models.TimeField(
        default="17:00",
    )

    ATTENDANCE_METHOD_CHOICES = [
        ("manual", "Manual Entry"),
        ("biometric", "Biometric"),
        ("qr", "QR Code"),
        ("web", "Web Check-in"),
        ("mobile", "Mobile Check-in"),
    ]

    attendance_method = models.CharField(
        max_length=20,
        choices=ATTENDANCE_METHOD_CHOICES,
        default="manual",
    )

    SALARY_CYCLE_CHOICES = [
        ("monthly", "Monthly"),
        ("weekly", "Weekly"),
    ]

    salary_cycle = models.CharField(
        max_length=20,
        choices=SALARY_CYCLE_CHOICES,
        default="monthly",
    )

    OVERTIME_CHOICES = [
        ("disabled", "Disabled"),
        ("hourly", "Hourly Rate"),
        ("fixed", "Fixed Overtime Rate"),
        ("percentage", "Percentage of Hourly Rate"),
    ]

    overtime_calculation = models.CharField(
        max_length=20,
        choices=OVERTIME_CHOICES,
        default="disabled",
    )

    overtime_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
        ],
    )


    annual_leave = models.PositiveIntegerField(
        default=12,
        validators=[
            MaxValueValidator(365),
        ],
    )

    sick_leave = models.PositiveIntegerField(
        default=12,
        validators=[
            MaxValueValidator(365),
        ],
    )

    leave_carry_forward = models.BooleanField(
        default=True,
    )


    employee_prefix = models.CharField(
        max_length=10,
        default="EMP",
    )

    auto_employee_id = models.BooleanField(
        default=True,
    )

    starting_number = models.PositiveIntegerField(
        default=1,
    )

    probation_period = models.PositiveIntegerField(
        default=6,
        validators=[
            MaxValueValidator(60),
        ],
    )

    probation_tracking = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Employee Setting"
        verbose_name_plural = "Employee Settings"

    def __str__(self):

        return (
            f"Employee Settings - "
            f"{self.company.company_name}"
        )




class StudentSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="student_settings"
    )

    # Student Identification

    admission_prefix = models.CharField(
        max_length=20,
        default="ADM",
        blank=True
    )

    student_id_format = models.CharField(
        max_length=50,
        default="PREFIX-YEAR-NUMBER"
    )

    auto_generate_student_id = models.BooleanField(
        default=True
    )

    default_student_status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("pending", "Pending"),
            ("inactive", "Inactive"),
        ],
        default="active"
    )

    # Academic Settings

    course_duration = models.PositiveIntegerField(
        default=12
    )

    course_duration_unit = models.CharField(
        max_length=20,
        choices=[
            ("months", "Months"),
            ("years", "Years"),
        ],
        default="months"
    )

    default_course = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    # Attendance Settings

    attendance_tracking = models.BooleanField(
        default=True
    )

    attendance_alerts = models.BooleanField(
        default=False
    )

    # Fee Reminder Settings

    fee_reminders = models.BooleanField(
        default=False
    )

    fee_reminder_schedule = models.CharField(
        max_length=30,
        choices=[
            ("none", "No Reminder"),
            ("before_7", "7 Days Before Due Date"),
            ("before_3", "3 Days Before Due Date"),
            ("before_1", "1 Day Before Due Date"),
            ("on_due", "On Due Date"),
            ("after_3", "3 Days After Due Date"),
        ],
        default="none"
    )

    # Certificate Settings

    certificate_number_format = models.CharField(
        max_length=50,
        default="CERT-YEAR-NUMBER"
    )

    certificate_prefix = models.CharField(
        max_length=20,
        default="CERT"
    )

    # Parent Notification Settings

    parent_notifications = models.BooleanField(
        default=False
    )

    notify_fee = models.BooleanField(
        default=False
    )

    notify_attendance = models.BooleanField(
        default=False
    )

    notify_certificate = models.BooleanField(
        default=False
    )

    notify_general = models.BooleanField(
        default=False
    )

    # Timestamps

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.company} - Student Settings"

class NotificationSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="notification_settings"
    )

    # Notification Channels
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    whatsapp_notifications = models.BooleanField(default=False)

    # Alert Preferences
    fee_due_reminders = models.BooleanField(default=True)
    salary_payment_notifications = models.BooleanField(default=True)
    attendance_alerts = models.BooleanField(default=True)
    student_admission_alerts = models.BooleanField(default=True)
    employee_joining_alerts = models.BooleanField(default=True)
    invoice_payment_reminders = models.BooleanField(default=True)
    monthly_summary_reports = models.BooleanField(default=True)

    # Reminder Configuration
    fee_reminder_days = models.PositiveIntegerField(default=7)
    invoice_reminder_days = models.PositiveIntegerField(default=7)
    summary_day = models.PositiveIntegerField(default=1)

    notification_time = models.TimeField(
        default="09:00"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Notification Settings - {self.company.company_name}"




class AppearanceSettings(models.Model):

    THEME_CHOICES = (
        ("light", "Light"),
        ("dark", "Dark"),
    )

    FONT_SIZE_CHOICES = (
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    )

    DASHBOARD_LAYOUT_CHOICES = (
        ("grid", "Grid Layout"),
        ("compact", "Compact Layout"),
        ("wide", "Wide Layout"),
    )

    SIDEBAR_STYLE_CHOICES = (
        ("expanded", "Expanded"),
        ("compact", "Compact"),
        ("collapsed", "Collapsed"),
    )

    LANGUAGE_CHOICES = (
        ("en", "English"),
        ("ml", "Malayalam"),
        ("hi", "Hindi"),
        ("ta", "Tamil"),
    )

    DATE_FORMAT_CHOICES = (
        ("DD/MM/YYYY", "DD/MM/YYYY"),
        ("MM/DD/YYYY", "MM/DD/YYYY"),
        ("YYYY-MM-DD", "YYYY-MM-DD"),
    )

    TIME_FORMAT_CHOICES = (
        ("12", "12 Hour"),
        ("24", "24 Hour"),
    )

    TIMEZONE_CHOICES = (
        ("Asia/Kolkata", "India Standard Time (IST)"),
        ("UTC", "UTC"),
        ("America/New_York", "Eastern Time"),
        ("Europe/London", "London Time"),
    )

    # One appearance settings record for each company
    company = models.OneToOneField(
        "app.Company",
        on_delete=models.CASCADE,
        related_name="appearance_settings",
    )

    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default="light",
    )

    accent_color = models.CharField(
        max_length=7,
        default="#2563eb",
    )

    font_size = models.CharField(
        max_length=10,
        choices=FONT_SIZE_CHOICES,
        default="medium",
    )

    dashboard_layout = models.CharField(
        max_length=20,
        choices=DASHBOARD_LAYOUT_CHOICES,
        default="grid",
    )

    sidebar_style = models.CharField(
        max_length=20,
        choices=SIDEBAR_STYLE_CHOICES,
        default="expanded",
    )

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default="en",
    )

    date_format = models.CharField(
        max_length=20,
        choices=DATE_FORMAT_CHOICES,
        default="DD/MM/YYYY",
    )

    time_format = models.CharField(
        max_length=5,
        choices=TIME_FORMAT_CHOICES,
        default="12",
    )

    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default="Asia/Kolkata",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.company.company_name} Appearance Settings"
class ReportSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="report_settings",
    )

    default_report_format = models.CharField(
        max_length=10,
        choices=(
            ("pdf", "PDF"),
            ("excel", "Excel"),
        ),
        default="pdf",
    )

    default_date_range = models.CharField(
        max_length=20,
        choices=(
            ("today", "Today"),
            ("this_week", "This Week"),
            ("this_month", "This Month"),
            ("last_month", "Last Month"),
            ("this_year", "This Year"),
            ("custom", "Custom Range"),
        ),
        default="this_month",
    )

    include_company_logo = models.BooleanField(
        default=True
    )

    show_gst_details = models.BooleanField(
        default=True
    )

    include_signature = models.BooleanField(
        default=False
    )

    report_header_footer = models.BooleanField(
        default=True
    )

    report_watermark = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    enable_watermark = models.BooleanField(
        default=False
    )

    watermark_position = models.CharField(
        max_length=10,
        choices=(
            ("center", "Center"),
            ("top", "Top"),
            ("bottom", "Bottom"),
        ),
        default="center",
    )

    automatic_monthly_reports = models.BooleanField(
        default=False
    )

    email_reports_to_admin = models.BooleanField(
        default=False
    )

    monthly_report_day = models.PositiveSmallIntegerField(
        default=1
    )

    monthly_report_time = models.TimeField(
        default="09:00"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Report Settings - {self.company.company_name}"

class UserPermission(models.Model):

    MODULE_CHOICES = [
        ("dashboard", "Dashboard"),
        ("students", "Students"),
        ("employees", "Employees"),
        ("billing", "Billing"),
        ("reports", "Reports"),
        ("certificates", "Certificates"),
        ("settings", "Settings"),
    ]

    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="permissions"
    )

    module = models.CharField(
        max_length=50,
        choices=MODULE_CHOICES
    )

    can_view = models.BooleanField(
        default=True
    )

    can_add = models.BooleanField(
        default=False
    )

    can_edit = models.BooleanField(
        default=False
    )

    can_delete = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            "user_profile",
            "module"
        )

    def __str__(self):
        return (
            f"{self.user_profile.user.username} - "
            f"{self.get_module_display()}"
        )


