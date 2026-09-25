from django.db import models
from app.models import Company
from employees.models import Employee
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal






class Salary(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="salary_records"
    )


    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salary_records"
    )


    month = models.CharField(
        max_length=20
    )


    year = models.IntegerField()


    basic = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    allowance = models.DecimalField(
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
        decimal_places=2,
        default=0
    )


    paid = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def save(self, *args, **kwargs):

        self.net_salary = (
            self.basic +
            self.allowance -
            self.deduction
        )

        super().save(*args, **kwargs)


    def __str__(self):

        return f"{self.employee.name} - {self.month} {self.year}"




class Employee(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="salary_employees"
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=50,
        default="Active"
    )


    joined_date = models.DateField(
        blank=True,
        null=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.name




class SalaryStructure(models.Model):

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="salary_structures"
    )


    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salary_structures"
    )


    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    hra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    allowance = models.DecimalField(
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
        decimal_places=2,
        default=0
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def save(self,*args,**kwargs):

        self.net_salary = (
            self.basic_salary
            +
            self.hra
            +
            self.allowance
            -
            self.deduction
        )

        super().save(*args,**kwargs)



    def __str__(self):

        return self.employee.name




class Payroll(models.Model):

    STATUS = (
        ('Paid','Paid'),
        ('Pending','Pending'),
    )


    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="payrolls"
    )


    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payrolls"
    )


    month = models.CharField(
        max_length=20
    )


    year = models.IntegerField()


    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    allowance = models.DecimalField(
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
        choices=STATUS,
        default="Pending"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def save(self,*args,**kwargs):

        self.net_salary = (
            self.basic_salary
            +
            self.allowance
            -
            self.deduction
        )

        super().save(*args,**kwargs)



    def __str__(self):

        return f"{self.employee.name} - {self.month} {self.year}"




class Payslip(models.Model):


    company = models.ForeignKey(
    Company,
    on_delete=models.CASCADE,
    related_name="payslips"
)


    employee = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    related_name="payslips"
)


    month = models.CharField(
        max_length=20
    )


    year = models.IntegerField()



    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    allowance = models.DecimalField(
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
        decimal_places=2,
        default=0
    )



    payment_status=models.CharField(

        max_length=20,

        choices=(

            ("Paid","Paid"),

            ("Pending","Pending")

        ),

        default="Pending"

    )



    created_at=models.DateTimeField(
        auto_now_add=True
    )



    def save(self,*args,**kwargs):


        self.net_salary = (

            self.basic_salary

            +

            self.allowance

            -

            self.deduction

        )


        super().save(*args,**kwargs)



    def __str__(self):

        return self.employee.name




class Bonus(models.Model):


    company = models.ForeignKey(
    Company,
    on_delete=models.CASCADE,
    related_name="bonuses"
)


    employee = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    related_name="bonuses"
)


    bonus_title = models.CharField(
        max_length=100
    )


    bonus_type = models.CharField(
        max_length=50,
        choices=(

            ("Performance","Performance"),

            ("Festival","Festival"),

            ("Annual","Annual"),

            ("Other","Other"),

        )
    )


    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    bonus_date = models.DateField()



    description = models.TextField(
        blank=True,
        null=True
    )



    payment_status = models.CharField(

        max_length=20,

        choices=(

            ("Paid","Paid"),

            ("Pending","Pending"),

        ),

        default="Pending"

    )



    created_at = models.DateTimeField(
        auto_now_add=True
    )



    def __str__(self):

        return self.employee.name



class Deduction(models.Model):


    company = models.ForeignKey(
    Company,
    on_delete=models.CASCADE,
    related_name="deductions"
)


    employee = models.ForeignKey(
    Employee,
    on_delete=models.CASCADE,
    related_name="deductions"
)


    deduction_title = models.CharField(
        max_length=100
    )


    deduction_type = models.CharField(

        max_length=50,

        choices=(

            ("PF","PF"),

            ("ESI","ESI"),

            ("Tax","Tax"),

            ("Loan","Loan"),

            ("Other","Other"),

        )

    )


    amount = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )


    deduction_date = models.DateField()



    description = models.TextField(

        blank=True,

        null=True

    )


    status = models.CharField(

        max_length=20,

        choices=(

            ("Applied","Applied"),

            ("Completed","Completed"),

        ),

        default="Applied"

    )


    created_at=models.DateTimeField(

        auto_now_add=True

    )



    def __str__(self):

        return self.employee.name

class Attendance(models.Model):

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
            ("Leave", "Leave"),
            ("Half Day", "Half Day"),
        ]
    )

    check_in = models.TimeField(
        null=True,
        blank=True
    )

    check_out = models.TimeField(
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee} - {self.date}"

    
class SalaryPayrollSettings(models.Model):

    PAYROLL_CYCLE_CHOICES = [
        ("monthly", "Monthly"),
        ("weekly", "Weekly"),
        ("biweekly", "Bi-Weekly"),
    ]

    SALARY_PERIOD_CHOICES = [
        ("calendar_month", "Calendar Month"),
        ("attendance_period", "Attendance Period"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="payroll_settings"
    )

    payroll_cycle = models.CharField(
        max_length=30,
        choices=PAYROLL_CYCLE_CHOICES,
        default="monthly"
    )

    salary_period = models.CharField(
        max_length=30,
        choices=SALARY_PERIOD_CHOICES,
        default="calendar_month"
    )

    payment_day = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
    )

    working_days = models.PositiveIntegerField(
        default=26
    )

    overtime_enabled = models.BooleanField(
        default=True
    )

    overtime_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1.5
    )

    automatic_salary_calculation = models.BooleanField(
        default=True
    )

    attendance_based_salary = models.BooleanField(
        default=True
    )

    automatic_deductions = models.BooleanField(
        default=True
    )

    automatic_allowances = models.BooleanField(
        default=True
    )

    allow_negative_salary = models.BooleanField(
        default=False
    )

    payroll_approval_required = models.BooleanField(
        default=False
    )

    payslip_generation = models.BooleanField(
        default=True
    )

    payroll_notification = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.company.company_name} Payroll Settings"

class SalaryPayroll(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="salary_payrolls"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="salary_payrolls"
    )

    month = models.CharField(
        max_length=20
    )

    year = models.PositiveIntegerField()

    basic_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    allowance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    deduction = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-year", "-id"]

    def __str__(self):
        return (
            f"{self.employee.name} - "
            f"{self.month} {self.year}"
        )



class SalaryAttendanceSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="salary_attendance_settings"
    )

    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=False)


    work_start_time = models.TimeField(
        default="09:00"
    )

    work_end_time = models.TimeField(
        default="18:00"
    )

    break_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("1.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ]
    )

    late_mark_enabled = models.BooleanField(
        default=True
    )

    late_mark_minutes = models.PositiveIntegerField(
        default=15,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(180)
        ]
    )

    early_exit_enabled = models.BooleanField(
        default=True
    )

    early_exit_minutes = models.PositiveIntegerField(
        default=15,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(180)
        ]
    )

    overtime_enabled = models.BooleanField(
        default=True
    )

    overtime_after_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("8.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ]
    )

    half_day_enabled = models.BooleanField(
        default=True
    )

    half_day_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("4.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ]
    )

    auto_absent_enabled = models.BooleanField(
        default=False
    )

    leave_requires_approval = models.BooleanField(
        default=True
    )


    deduct_absence_from_salary = models.BooleanField(
        default=True
    )

    deduct_late_from_salary = models.BooleanField(
        default=False
    )

    include_overtime_in_salary = models.BooleanField(
        default=True
    )


    attendance_notifications = models.BooleanField(
        default=True
    )

    late_notifications = models.BooleanField(
        default=True
    )

    absence_notifications = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Salary Attendance Setting"
        verbose_name_plural = "Salary Attendance Settings"

    def __str__(self):
        return f"Attendance Settings - {self.company}"




class SalaryPayslipSettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="payslip_settings"
    )


    payslip_title = models.CharField(
        max_length=150,
        default="Salary Payslip"
    )

    payslip_subtitle = models.CharField(
        max_length=200,
        default="Employee Salary Statement"
    )

    currency_symbol = models.CharField(
        max_length=10,
        default="₹"
    )

    payslip_prefix = models.CharField(
        max_length=50,
        default="PAY"
    )

    payslip_number_format = models.CharField(
        max_length=100,
        default="PAY-{year}-{number}"
    )

    auto_generate_number = models.BooleanField(
        default=True
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

    show_company_logo = models.BooleanField(
        default=True
    )


    show_employee_id = models.BooleanField(
        default=True
    )

    show_employee_department = models.BooleanField(
        default=True
    )

    show_employee_designation = models.BooleanField(
        default=True
    )

    show_joining_date = models.BooleanField(
        default=True
    )


    show_basic_salary = models.BooleanField(
        default=True
    )

    show_allowance = models.BooleanField(
        default=True
    )

    show_deduction = models.BooleanField(
        default=True
    )

    show_net_salary = models.BooleanField(
        default=True
    )

    show_working_days = models.BooleanField(
        default=True
    )

    show_present_days = models.BooleanField(
        default=True
    )

    show_absent_days = models.BooleanField(
        default=True
    )

    show_leave_days = models.BooleanField(
        default=True
    )

    show_payment_status = models.BooleanField(
        default=True
    )

    show_payment_method = models.BooleanField(
        default=True
    )

    footer_text = models.CharField(
        max_length=300,
        default="This is a computer-generated payslip."
    )

    show_signature = models.BooleanField(
        default=True
    )

    authorized_person = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    authorized_designation = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    paper_size = models.CharField(
        max_length=20,
        choices=[
            ("A4", "A4"),
            ("LETTER", "Letter"),
            ("A5", "A5"),
        ],
        default="A4"
    )

    orientation = models.CharField(
        max_length=20,
        choices=[
            ("portrait", "Portrait"),
            ("landscape", "Landscape"),
        ],
        default="portrait"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Payslip Settings - {self.company}"


class SalaryTaxDeductionSettings(models.Model):

    CALCULATION_BASIS_CHOICES = [
        ("basic", "Basic Salary"),
        ("gross", "Gross Salary"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="salary_tax_deduction_settings"
    )

    enable_deductions = models.BooleanField(
        default=True
    )

    auto_apply_deductions = models.BooleanField(
        default=False
    )

    calculation_basis = models.CharField(
        max_length=20,
        choices=CALCULATION_BASIS_CHOICES,
        default="basic"
    )

    enable_pf = models.BooleanField(
        default=True
    )

    pf_employee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=12,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


    enable_esi = models.BooleanField(
        default=True
    )

    esi_employee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )


    enable_professional_tax = models.BooleanField(
        default=False
    )

    professional_tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )


    enable_income_tax = models.BooleanField(
        default=False
    )

    income_tax_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    enable_loan_deduction = models.BooleanField(
        default=True
    )

    enable_other_deductions = models.BooleanField(
        default=True
    )

    prevent_negative_salary = models.BooleanField(
        default=True
    )

    deduction_notifications = models.BooleanField(
        default=True
    )

    tax_notifications = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Tax & Deduction Settings - {self.company}"


class SalaryBonusSettings(models.Model):

    BONUS_TYPE_CHOICES = [
        ("Performance", "Performance"),
        ("Festival", "Festival"),
        ("Annual", "Annual"),
        ("Joining", "Joining"),
        ("Referral", "Referral"),
        ("Other", "Other"),
    ]

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="bonus_settings"
    )


    bonus_enabled = models.BooleanField(
        default=True
    )

    default_bonus_type = models.CharField(
        max_length=30,
        choices=BONUS_TYPE_CHOICES,
        default="Performance"
    )

    minimum_bonus_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    maximum_bonus_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    auto_include_in_payroll = models.BooleanField(
        default=True
    )

    require_approval = models.BooleanField(
        default=True
    )

    allow_manual_bonus = models.BooleanField(
        default=True
    )

    taxable_bonus = models.BooleanField(
        default=True
    )

    include_bonus_in_payslip = models.BooleanField(
        default=True
    )

    include_bonus_in_salary = models.BooleanField(
        default=True
    )


    notify_employee = models.BooleanField(
        default=True
    )

    notify_admin = models.BooleanField(
        default=True
    )


    performance_bonus_enabled = models.BooleanField(
        default=True
    )

    festival_bonus_enabled = models.BooleanField(
        default=True
    )

    annual_bonus_enabled = models.BooleanField(
        default=True
    )

    referral_bonus_enabled = models.BooleanField(
        default=True
    )

    default_description = models.TextField(
        blank=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Bonus Settings - {self.company}"

    class Meta:
        verbose_name = "Salary Bonus Settings"
        verbose_name_plural = "Salary Bonus Settings"





class EmployeeSalarySettings(models.Model):

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="employee_salary_settings"
    )


    salary_enabled = models.BooleanField(
        default=True
    )

    default_currency = models.CharField(
        max_length=10,
        default="₹"
    )

    salary_calculation_enabled = models.BooleanField(
        default=True
    )

    basic_salary_required = models.BooleanField(
        default=True
    )

    allow_zero_salary = models.BooleanField(
        default=False
    )

    allowance_enabled = models.BooleanField(
        default=True
    )

    default_allowance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )


    deduction_enabled = models.BooleanField(
        default=True
    )

    default_deduction = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )


    auto_calculate_net_salary = models.BooleanField(
        default=True
    )

    include_attendance = models.BooleanField(
        default=True
    )

    include_overtime = models.BooleanField(
        default=True
    )

    include_bonus = models.BooleanField(
        default=True
    )

    include_deductions = models.BooleanField(
        default=True
    )


    salary_from_joining_date = models.BooleanField(
        default=True
    )

    prorate_first_month_salary = models.BooleanField(
        default=True
    )

    default_payment_method = models.CharField(
        max_length=30,
        choices=[
            ("Bank Transfer", "Bank Transfer"),
            ("Cash", "Cash"),
            ("UPI", "UPI"),
            ("Cheque", "Cheque"),
        ],
        default="Bank Transfer"
    )


    salary_notifications = models.BooleanField(
        default=True
    )

    salary_update_notifications = models.BooleanField(
        default=True
    )

    salary_payment_notifications = models.BooleanField(
        default=True
    )


    allow_salary_edit = models.BooleanField(
        default=True
    )

    allow_salary_history = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Employee Salary Settings - {self.company}"



class SalaryNotificationSettings(models.Model):
    """
    Notification settings for the salary/payroll module.
    One configuration per company.
    """

    company = models.OneToOneField(
        "app.Company",
        on_delete=models.CASCADE,
        related_name="salary_notification_settings"
    )

    notifications_enabled = models.BooleanField(
        default=True
    )

    email_notifications = models.BooleanField(
        default=True
    )

    in_app_notifications = models.BooleanField(
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

    salary_updated_notification = models.BooleanField(
        default=True
    )


    payroll_processed_notification = models.BooleanField(
        default=True
    )

    payroll_failed_notification = models.BooleanField(
        default=True
    )

    payroll_reminder_notification = models.BooleanField(
        default=True
    )

    employee_salary_notification = models.BooleanField(
        default=True
    )

    employee_payment_notification = models.BooleanField(
        default=True
    )


    salary_reminder_days = models.PositiveIntegerField(
        default=3,
        help_text=(
            "Number of days before salary due date "
            "to send reminder."
        )
    )

    notify_admin = models.BooleanField(
        default=True
    )

    notify_manager = models.BooleanField(
        default=True
    )

    notify_employee = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Salary Notification Settings"
        verbose_name_plural = "Salary Notification Settings"

    def __str__(self):
        return (
            f"Salary Notification Settings - "
            f"{self.company}"
        )

class SalaryThemeSettings(models.Model):

    company = models.OneToOneField(
        "app.Company",
        on_delete=models.CASCADE,
        related_name="salary_theme_settings"
    )

    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("system", "System Default"),
    ]

    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default="light"
    )


    accent_color = models.CharField(
        max_length=20,
        default="#2563eb"
    )

    FONT_SIZE_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    font_size = models.CharField(
        max_length=20,
        choices=FONT_SIZE_CHOICES,
        default="medium"
    )

    DASHBOARD_LAYOUT_CHOICES = [
        ("grid", "Grid"),
        ("list", "List"),
        ("compact", "Compact"),
    ]

    dashboard_layout = models.CharField(
        max_length=20,
        choices=DASHBOARD_LAYOUT_CHOICES,
        default="grid"
    )

    SIDEBAR_STYLE_CHOICES = [
        ("expanded", "Expanded"),
        ("compact", "Compact"),
        ("collapsed", "Collapsed"),
    ]

    sidebar_style = models.CharField(
        max_length=20,
        choices=SIDEBAR_STYLE_CHOICES,
        default="expanded"
    )

    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("ml", "Malayalam"),
        ("hi", "Hindi"),
        ("ta", "Tamil"),
    ]

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default="en"
    )


    TIMEZONE_CHOICES = [
        ("Asia/Kolkata", "India - Kolkata"),
        ("Asia/Dubai", "UAE - Dubai"),
        ("Asia/Singapore", "Singapore"),
        ("Europe/London", "United Kingdom - London"),
        ("America/New_York", "USA - New York"),
        ("America/Los_Angeles", "USA - Los Angeles"),
    ]

    time_zone = models.CharField(
        max_length=100,
        choices=TIMEZONE_CHOICES,
        default="Asia/Kolkata"
    )

    show_breadcrumbs = models.BooleanField(
        default=True
    )

    show_page_description = models.BooleanField(
        default=True
    )

    compact_cards = models.BooleanField(
        default=False
    )

    animations_enabled = models.BooleanField(
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
            f"{self.company} - Salary Theme Settings"
        )