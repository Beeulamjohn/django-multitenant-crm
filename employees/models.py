from django.db import models
from app.models import Company
from django.contrib.auth.models import User


class Employee(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Resigned", "Resigned"),
        ("Terminated", "Terminated"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employees"
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile"
    )

    employee_id = models.CharField(
        max_length=20
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    gender = models.CharField(
        max_length=20,
        blank=True
    )

    dob = models.DateField(
        null=True,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    role = models.CharField(
        max_length=100,
        blank=True
    )

    department = models.CharField(
        max_length=100,
        blank=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True
    )

    joining_date = models.DateField(
        null=True,
        blank=True
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    employment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()
    
class Attendance(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_attendance"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("Present", "Present"),
            ("Absent", "Absent"),
            ("Late", "Late"),
            ("Leave", "Leave"),
        ]
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["employee", "date"],
                name="unique_employee_attendance_date"
            )
        ]

    def __str__(self):
        return f"{self.employee} - {self.date}"


class Payroll(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_payroll"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payroll_records"
    )

    month = models.CharField(
        max_length=20
    )

    year = models.IntegerField()

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    bonus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("Paid", "Paid"),
            ("Pending", "Pending"),
        ],
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["employee", "month", "year"],
                name="unique_employee_payroll_month"
            )
        ]

    def __str__(self):
        return f"{self.employee} - {self.month} {self.year}"


class Staff(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="staffs"
    )

    staff_id = models.CharField(
        max_length=30
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    designation = models.CharField(
        max_length=100
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    joining_date = models.DateField()

    status = models.CharField(
        max_length=20,
        default="Active"
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "staff_id"
                ],
                name="unique_staff_id_company"
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class EmployeeDataSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_data_settings"
    )

    employee_id_prefix = models.CharField(
        max_length=20,
        default="EMP"
    )

    employee_id_format = models.CharField(
        max_length=100,
        default="EMP-{year}-{number}"
    )

    auto_generate_employee_id = models.BooleanField(
        default=True
    )

    default_employment_status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive"),
            ("Resigned", "Resigned"),
            ("Terminated", "Terminated"),
        ],
        default="Active"
    )

    default_department = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    default_role = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    attendance_tracking = models.BooleanField(
        default=True
    )

    attendance_alerts = models.BooleanField(
        default=True
    )

    late_arrival_tracking = models.BooleanField(
        default=True
    )

    overtime_tracking = models.BooleanField(
        default=True
    )

    payroll_enabled = models.BooleanField(
        default=True
    )

    salary_currency = models.CharField(
        max_length=10,
        default="INR"
    )

    salary_cycle = models.CharField(
        max_length=30,
        choices=[
            ("Monthly", "Monthly"),
            ("Weekly", "Weekly"),
            ("Biweekly", "Biweekly"),
        ],
        default="Monthly"
    )

    employee_notifications = models.BooleanField(
        default=True
    )

    attendance_notifications = models.BooleanField(
        default=True
    )

    payroll_notifications = models.BooleanField(
        default=True
    )

    leave_notifications = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Employee Settings - {self.company.company_name}"

class EmployeeCompanyProfile(models.Model):
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_company_profile"
    )

    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(
        upload_to="employee/company_logos/",
        blank=True,
        null=True
    )

    COMPANY_TYPES = [
        ("private", "Private Limited"),
        ("public", "Public Limited"),
        ("llp", "LLP"),
        ("partnership", "Partnership"),
        ("proprietorship", "Proprietorship"),
        ("other", "Other"),
    ]

    company_type = models.CharField(
        max_length=30,
        choices=COMPANY_TYPES,
        default="private"
    )

    owner_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")
    pin_code = models.CharField(max_length=10)

    gst_number = models.CharField(max_length=15, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Employee Company Profile"
        verbose_name_plural = "Employee Company Profiles"

    def __str__(self):
        return self.company_name
class EmployeeDepartmentSettings(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="department_settings"
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
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
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="employee_department_company_name_unique"
            )
        ]

    def __str__(self):
        return self.name


class EmployeeRoleData(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_role_settings"
    )

    department = models.ForeignKey(
        EmployeeDepartmentSettings,
        on_delete=models.CASCADE,
        related_name="roles"
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
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

        ordering = [
            "department__name",
            "name"
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "department",
                    "name"
                ],
                name="employee_role_company_department_name_unique"
            )
        ]

    def __str__(self):
        return f"{self.department.name} - {self.name}"

class EmployeeAttendanceSettings(models.Model):
    """
    Company-level attendance configuration.
    One company has one attendance settings record.
    """

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_attendance_settings"
    )


    attendance_tracking = models.BooleanField(
        default=True
    )

    attendance_method = models.CharField(
        max_length=30,
        choices=[
            ("Manual", "Manual"),
            ("Biometric", "Biometric"),
            ("Self", "Employee Self Check-in"),
        ],
        default="Manual"
    )

    allow_employee_checkin = models.BooleanField(
        default=False
    )

    allow_employee_checkout = models.BooleanField(
        default=False
    )


    work_start_time = models.TimeField(
        default="09:00"
    )

    work_end_time = models.TimeField(
        default="18:00"
    )

    late_after_minutes = models.PositiveIntegerField(
        default=15
    )

    half_day_after_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=4
    )

    full_day_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=8
    )

    monday = models.BooleanField(
        default=True
    )

    tuesday = models.BooleanField(
        default=True
    )

    wednesday = models.BooleanField(
        default=True
    )

    thursday = models.BooleanField(
        default=True
    )

    friday = models.BooleanField(
        default=True
    )

    saturday = models.BooleanField(
        default=False
    )

    sunday = models.BooleanField(
        default=False
    )

    late_arrival_tracking = models.BooleanField(
        default=True
    )

    automatic_absent = models.BooleanField(
        default=True
    )

    automatic_absent_after_minutes = models.PositiveIntegerField(
        default=120
    )

    overtime_tracking = models.BooleanField(
        default=True
    )

    overtime_after_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=8
    )

    attendance_alerts = models.BooleanField(
        default=True
    )

    late_arrival_alerts = models.BooleanField(
        default=True
    )

    absence_alerts = models.BooleanField(
        default=True
    )

    employee_attendance_notifications = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Attendance Settings - {self.company.company_name}"



class EmployeeLeaveSettings(models.Model):
    """
    Company-level leave configuration.
    One company has one leave-settings record.
    """

    LEAVE_YEAR_CHOICES = [
        ("calendar", "Calendar Year (January - December)"),
        ("financial", "Financial Year (April - March)"),
    ]

    ACCRUAL_CHOICES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_leave_settings",
    )


    enable_leave_management = models.BooleanField(
        default=True
    )

    leave_year_type = models.CharField(
        max_length=20,
        choices=LEAVE_YEAR_CHOICES,
        default="calendar",
    )

    allow_employee_leave_request = models.BooleanField(
        default=True
    )

    require_leave_reason = models.BooleanField(
        default=True
    )

    require_approval = models.BooleanField(
        default=True
    )

    annual_leave_days = models.PositiveIntegerField(
        default=12
    )

    sick_leave_days = models.PositiveIntegerField(
        default=12
    )

    casual_leave_days = models.PositiveIntegerField(
        default=12
    )

    unpaid_leave_allowed = models.BooleanField(
        default=True
    )

    carry_forward_enabled = models.BooleanField(
        default=False
    )

    carry_forward_days = models.PositiveIntegerField(
        default=0
    )


    leave_accrual = models.CharField(
        max_length=20,
        choices=ACCRUAL_CHOICES,
        default="monthly",
    )

    manager_approval = models.BooleanField(
        default=True
    )

    hr_approval = models.BooleanField(
        default=False
    )

    admin_approval = models.BooleanField(
        default=False
    )


    employee_notifications = models.BooleanField(
        default=True
    )

    manager_notifications = models.BooleanField(
        default=True
    )

    hr_notifications = models.BooleanField(
        default=True
    )

    leave_reminder_notifications = models.BooleanField(
        default=True
    )


    minimum_notice_days = models.PositiveIntegerField(
        default=1
    )

    maximum_consecutive_days = models.PositiveIntegerField(
        default=30
    )

    allow_backdated_leave = models.BooleanField(
        default=False
    )

    allow_half_day_leave = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Leave Settings - {self.company.company_name}"

class EmployeePayrollSettings(models.Model):
    """
    Company-level payroll configuration.
    One payroll settings record per company.
    """

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_payroll_settings"
    )


    payroll_enabled = models.BooleanField(
        default=True
    )

    auto_calculate_salary = models.BooleanField(
        default=True
    )

    PAYROLL_CYCLE_CHOICES = [
        ("Monthly", "Monthly"),
        ("Weekly", "Weekly"),
        ("Biweekly", "Biweekly"),
    ]

    payroll_cycle = models.CharField(
        max_length=20,
        choices=PAYROLL_CYCLE_CHOICES,
        default="Monthly"
    )

    payroll_day = models.PositiveIntegerField(
        default=1,
        help_text="Day of month on which payroll is processed."
    )

    currency = models.CharField(
        max_length=10,
        default="INR"
    )

    currency_symbol = models.CharField(
        max_length=5,
        default="₹"
    )

    include_basic_salary = models.BooleanField(
        default=True
    )

    include_allowances = models.BooleanField(
        default=True
    )

    include_bonus = models.BooleanField(
        default=True
    )

    include_deductions = models.BooleanField(
        default=True
    )

    include_overtime = models.BooleanField(
        default=True
    )


    attendance_based_salary = models.BooleanField(
        default=True
    )

    unpaid_leave_deduction = models.BooleanField(
        default=True
    )

    late_deduction = models.BooleanField(
        default=False
    )

    overtime_enabled = models.BooleanField(
        default=True
    )

    tax_deduction_enabled = models.BooleanField(
        default=False
    )

    provident_fund_enabled = models.BooleanField(
        default=False
    )

    professional_tax_enabled = models.BooleanField(
        default=False
    )

    payslip_enabled = models.BooleanField(
        default=True
    )

    payslip_company_name = models.BooleanField(
        default=True
    )

    payslip_employee_id = models.BooleanField(
        default=True
    )

    payslip_department = models.BooleanField(
        default=True
    )

    payslip_designation = models.BooleanField(
        default=True
    )

    payslip_attendance = models.BooleanField(
        default=True
    )

    payslip_salary_breakdown = models.BooleanField(
        default=True
    )


    payroll_notification = models.BooleanField(
        default=True
    )

    payslip_notification = models.BooleanField(
        default=True
    )

    payment_reminder = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Payroll Settings - {self.company.company_name}"



class EmployeeTaxSettings(models.Model):
    """
    Company-level tax and statutory configuration
    for the Employee Management module.
    """

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_tax_settings"
    )


    enable_tax_settings = models.BooleanField(
        default=True
    )

    tax_country = models.CharField(
        max_length=100,
        default="India"
    )

    financial_year = models.CharField(
        max_length=20,
        default="2026-27"
    )

    currency = models.CharField(
        max_length=10,
        default="INR"
    )

    pf_enabled = models.BooleanField(
        default=True
    )

    pf_employee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=12.00
    )

    pf_employer_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=12.00
    )

    pf_account_number = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    esi_enabled = models.BooleanField(
        default=False
    )

    esi_employee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.75
    )

    esi_employer_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=3.25
    )

    esi_number = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    professional_tax_enabled = models.BooleanField(
        default=False
    )

    professional_tax_state = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    professional_tax_number = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    tds_enabled = models.BooleanField(
        default=True
    )

    tan_number = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    tds_deduction_method = models.CharField(
        max_length=30,
        choices=[
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("annual", "Annual"),
        ],
        default="monthly"
    )

    labour_welfare_enabled = models.BooleanField(
        default=False
    )

    gratuity_enabled = models.BooleanField(
        default=False
    )

    bonus_enabled = models.BooleanField(
        default=False
    )


    statutory_reminders = models.BooleanField(
        default=True
    )

    compliance_notifications = models.BooleanField(
        default=True
    )

    payroll_tax_notifications = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Employee Tax & Statutory Settings"
        verbose_name_plural = "Employee Tax & Statutory Settings"

    def __str__(self):
        return f"Tax Settings - {self.company.company_name}"




class EmployeeNotificationSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_notification_settings"
    )

    employee_notifications = models.BooleanField(
        default=True
    )

    admin_notifications = models.BooleanField(
        default=True
    )

    manager_notifications = models.BooleanField(
        default=True
    )


    new_employee_notification = models.BooleanField(
        default=True
    )

    employee_profile_update_notification = models.BooleanField(
        default=True
    )

    employee_status_change_notification = models.BooleanField(
        default=True
    )

    employee_document_notification = models.BooleanField(
        default=True
    )

    attendance_notifications = models.BooleanField(
        default=True
    )

    late_arrival_notifications = models.BooleanField(
        default=True
    )

    absent_notifications = models.BooleanField(
        default=True
    )

    overtime_notifications = models.BooleanField(
        default=True
    )


    leave_notifications = models.BooleanField(
        default=True
    )

    leave_request_notification = models.BooleanField(
        default=True
    )

    leave_approval_notification = models.BooleanField(
        default=True
    )

    leave_rejection_notification = models.BooleanField(
        default=True
    )


    payroll_notifications = models.BooleanField(
        default=True
    )

    salary_generated_notification = models.BooleanField(
        default=True
    )

    salary_paid_notification = models.BooleanField(
        default=True
    )

    salary_pending_notification = models.BooleanField(
        default=True
    )

    document_expiry_notification = models.BooleanField(
        default=True
    )

    document_upload_notification = models.BooleanField(
        default=True
    )


    email_notifications = models.BooleanField(
        default=True
    )

    in_app_notifications = models.BooleanField(
        default=True
    )


    reminder_days = models.PositiveIntegerField(
        default=3
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Employee Notification Settings"
        verbose_name_plural = "Employee Notification Settings"

    def __str__(self):
        return (
            f"Employee Notification Settings - "
            f"{self.company.company_name}"
        )


class EmployeeDocumentSettings(models.Model):
    """
    Company-level settings for employee documents.
    One company has one document-settings record.
    """

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_document_settings"
    )
    enable_identity_documents = models.BooleanField(
        default=True
    )

    enable_address_documents = models.BooleanField(
        default=True
    )

    enable_education_documents = models.BooleanField(
        default=True
    )

    enable_experience_documents = models.BooleanField(
        default=True
    )

    enable_bank_documents = models.BooleanField(
        default=True
    )

    enable_contract_documents = models.BooleanField(
        default=True
    )

    enable_other_documents = models.BooleanField(
        default=True
    )

    require_identity_document = models.BooleanField(
        default=False
    )

    require_education_document = models.BooleanField(
        default=False
    )

    require_experience_document = models.BooleanField(
        default=False
    )

    require_bank_document = models.BooleanField(
        default=False
    )

    require_contract_document = models.BooleanField(
        default=False
    )

    allow_employee_upload = models.BooleanField(
        default=True
    )

    allow_employee_delete = models.BooleanField(
        default=False
    )

    admin_approval_required = models.BooleanField(
        default=True
    )

    max_file_size_mb = models.PositiveIntegerField(
        default=5
    )

    allowed_file_types = models.CharField(
        max_length=255,
        default="PDF, JPG, JPEG, PNG"
    )

    notify_admin_on_upload = models.BooleanField(
        default=True
    )

    notify_employee_on_approval = models.BooleanField(
        default=True
    )

    notify_employee_on_rejection = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Employee Document Settings"
        verbose_name_plural = "Employee Document Settings"

    def __str__(self):
        return (
            f"Employee Document Settings - "
            f"{self.company.company_name}"
        )




class EmployeeReportSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_report_settings"
    )

    employee_report = models.BooleanField(
        default=True
    )

    attendance_report = models.BooleanField(
        default=True
    )

    leave_report = models.BooleanField(
        default=True
    )

    payroll_report = models.BooleanField(
        default=True
    )

    salary_report = models.BooleanField(
        default=True
    )

    department_report = models.BooleanField(
        default=True
    )

    employee_performance_report = models.BooleanField(
        default=True
    )

    employee_document_report = models.BooleanField(
        default=True
    )


    show_employee_summary = models.BooleanField(
        default=True
    )

    show_department_summary = models.BooleanField(
        default=True
    )

    show_attendance_summary = models.BooleanField(
        default=True
    )

    show_leave_summary = models.BooleanField(
        default=True
    )

    show_payroll_summary = models.BooleanField(
        default=True
    )

    allow_employee_reports = models.BooleanField(
        default=False
    )

    allow_manager_reports = models.BooleanField(
        default=True
    )

    allow_admin_reports = models.BooleanField(
        default=True
    )


    allow_pdf_export = models.BooleanField(
        default=True
    )

    allow_excel_export = models.BooleanField(
        default=True
    )

    allow_csv_export = models.BooleanField(
        default=True
    )

    default_report_period = models.CharField(
        max_length=30,
        choices=[
            ("today", "Today"),
            ("week", "This Week"),
            ("month", "This Month"),
            ("quarter", "This Quarter"),
            ("year", "This Year"),
        ],
        default="month"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Employee Report Settings"
        verbose_name_plural = "Employee Report Settings"

    def __str__(self):
        return (
            f"Employee Report Settings - "
            f"{self.company.company_name}"
        )


class EmployeeSecuritySettings(models.Model):
    """
    Company-level security and permission settings
    for the Employee Management module.
    """

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_security_settings"
    )

    employee_login_enabled = models.BooleanField(
        default=True
    )

    allow_employee_portal = models.BooleanField(
        default=True
    )

    allow_employee_self_login = models.BooleanField(
        default=True
    )

    require_login_for_employee_portal = models.BooleanField(
        default=True
    )


    password_min_length = models.PositiveIntegerField(
        default=8
    )

    require_strong_password = models.BooleanField(
        default=True
    )

    password_expiry_enabled = models.BooleanField(
        default=False
    )

    password_expiry_days = models.PositiveIntegerField(
        default=90
    )


    session_timeout_enabled = models.BooleanField(
        default=True
    )

    session_timeout_minutes = models.PositiveIntegerField(
        default=30
    )

    allow_multiple_sessions = models.BooleanField(
        default=True
    )


    allow_profile_edit = models.BooleanField(
        default=True
    )

    allow_attendance_view = models.BooleanField(
        default=True
    )

    allow_leave_view = models.BooleanField(
        default=True
    )

    allow_payroll_view = models.BooleanField(
        default=False
    )

    allow_document_view = models.BooleanField(
        default=True
    )

    allow_report_view = models.BooleanField(
        default=False
    )

    require_admin_approval_for_profile_changes = models.BooleanField(
        default=False
    )

    require_admin_approval_for_leave = models.BooleanField(
        default=True
    )

    require_admin_approval_for_documents = models.BooleanField(
        default=False
    )

    notify_login = models.BooleanField(
        default=True
    )

    notify_password_change = models.BooleanField(
        default=True
    )

    notify_security_changes = models.BooleanField(
        default=True
    )


    enable_security_audit_log = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Employee Security Settings"
        verbose_name_plural = "Employee Security Settings"

    def __str__(self):
        return f"Employee Security Settings - {self.company}"


class EmployeeThemeSettings(models.Model):

    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
    ]

    FONT_SIZE_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    SIDEBAR_STYLE_CHOICES = [
        ("expanded", "Expanded"),
        ("compact", "Compact"),
    ]

    DASHBOARD_LAYOUT_CHOICES = [
        ("grid", "Grid"),
        ("list", "List"),
        ("comfortable", "Comfortable"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_theme_settings"
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

    font_size = models.CharField(
        max_length=20,
        choices=FONT_SIZE_CHOICES,
        default="medium"
    )

    sidebar_style = models.CharField(
        max_length=20,
        choices=SIDEBAR_STYLE_CHOICES,
        default="expanded"
    )

    dashboard_layout = models.CharField(
        max_length=20,
        choices=DASHBOARD_LAYOUT_CHOICES,
        default="grid"
    )

    compact_mode = models.BooleanField(
        default=False
    )

    reduced_motion = models.BooleanField(
        default=False
    )

    show_breadcrumbs = models.BooleanField(
        default=True
    )

    show_company_name = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Employee Theme Setting"
        verbose_name_plural = "Employee Theme Settings"

    def __str__(self):
        return f"Employee Theme Settings - {self.company}"