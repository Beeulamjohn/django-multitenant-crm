from django import forms
from .models import Employee
from .models import SalaryStructure
from .models import (
    SalaryPayrollSettings,
    SalaryPayroll,
)
from .models import (
    SalaryAttendanceSettings,
    Attendance,
)
from .models import SalaryPayslipSettings

from .models import (
    SalaryTaxDeductionSettings,
)
from .models import SalaryBonusSettings
from .models import EmployeeSalarySettings 
from .models import SalaryNotificationSettings
from .models import SalaryThemeSettings



class EmployeeForm(forms.ModelForm):

    class Meta:

        model = Employee


        fields = [
            "employee_id",
            "name",
            "department",
            "designation",
            "basic_salary",
            "status",
            "joined_date",
        ]


        widgets = {

            "employee_id":forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Employee ID"
                }
            ),


            "name":forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Employee Name"
                }
            ),


            "department":forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Department"
                }
            ),


            "designation":forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Designation"
                }
            ),


            "basic_salary":forms.NumberInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Basic Salary"
                }
            ),


            "status":forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Active / Inactive"
                }
            ),


            "joined_date":forms.DateInput(
                attrs={
                    "class":"form-control",
                    "type":"date"
                }
            ),

        }






class SalaryStructureForm(forms.ModelForm):


    class Meta:

        model = SalaryStructure


        fields = [

            "employee",
            "basic_salary",
            "hra",
            "allowance",
            "deduction",

        ]


        widgets={


            "employee":forms.Select(
                attrs={
                    "class":"form-control"
                }
            ),


            "basic_salary":forms.NumberInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Basic Salary"
                }
            ),


            "hra":forms.NumberInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"HRA"
                }
            ),


            "allowance":forms.NumberInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Allowance"
                }
            ),


            "deduction":forms.NumberInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Deduction"
                }
            ),


        }


class PayrollSettingsForm(forms.ModelForm):

    class Meta:
        model = SalaryPayrollSettings

        fields = [
            "payroll_cycle",
            "salary_period",
            "payment_day",
            "working_days",
            "overtime_enabled",
            "overtime_rate",
            "automatic_salary_calculation",
            "attendance_based_salary",
            "automatic_deductions",
            "automatic_allowances",
            "allow_negative_salary",
            "payroll_approval_required",
            "payslip_generation",
            "payroll_notification",
        ]

        widgets = {

            "payroll_cycle": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "salary_period": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "payment_day": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "max": "31"
                }
            ),

            "working_days": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "max": "31"
                }
            ),

            "overtime_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "overtime_enabled": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "automatic_salary_calculation": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "attendance_based_salary": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "automatic_deductions": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "automatic_allowances": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "allow_negative_salary": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "payroll_approval_required": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "payslip_generation": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),

            "payroll_notification": forms.CheckboxInput(
                attrs={
                    "class": "switch-input"
                }
            ),
        }

class SalaryPayrollForm(forms.ModelForm):

    class Meta:

        model = SalaryPayroll

        fields = [
            "employee",
            "month",
            "year",
            "basic_salary",
            "allowance",
            "deduction",
        ]

        widgets = {

            # Employee

            "employee": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),


            # Month

            "month": forms.Select(
                choices=[
                    ("January", "January"),
                    ("February", "February"),
                    ("March", "March"),
                    ("April", "April"),
                    ("May", "May"),
                    ("June", "June"),
                    ("July", "July"),
                    ("August", "August"),
                    ("September", "September"),
                    ("October", "October"),
                    ("November", "November"),
                    ("December", "December"),
                ],
                attrs={
                    "class": "form-control",
                }
            ),


            # Year

            "year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "2000",
                    "max": "2100",
                }
            ),


            # Basic Salary

            "basic_salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Enter basic salary",
                }
            ),


            # Allowance

            "allowance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Enter allowance",
                }
            ),


            # Deduction

            "deduction": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Enter deduction",
                }
            ),
        }

        
class SalaryAttendanceSettingsForm(forms.ModelForm):

    class Meta:

        model = SalaryAttendanceSettings

        fields = [
            # Working days
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",

            # Working hours
            "work_start_time",
            "work_end_time",
            "break_hours",

            # Late / early
            "late_mark_enabled",
            "late_mark_minutes",
            "early_exit_enabled",
            "early_exit_minutes",

            # Overtime
            "overtime_enabled",
            "overtime_after_hours",

            # Attendance status
            "half_day_enabled",
            "half_day_hours",
            "auto_absent_enabled",
            "leave_requires_approval",

            # Salary
            "deduct_absence_from_salary",
            "deduct_late_from_salary",
            "include_overtime_in_salary",

            # Notifications
            "attendance_notifications",
            "late_notifications",
            "absence_notifications",
        ]

        widgets = {


            "work_start_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "work_end_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "break_hours": forms.NumberInput(
                attrs={
                    "type": "number",
                    "step": "0.25",
                    "min": "0",
                    "class": "form-control",
                }
            ),

            "overtime_after_hours": forms.NumberInput(
                attrs={
                    "type": "number",
                    "step": "0.25",
                    "min": "0",
                    "class": "form-control",
                }
            ),

            "half_day_hours": forms.NumberInput(
                attrs={
                    "type": "number",
                    "step": "0.25",
                    "min": "0",
                    "class": "form-control",
                }
            ),


            "late_mark_minutes": forms.NumberInput(
                attrs={
                    "type": "number",
                    "min": "0",
                    "max": "180",
                    "class": "form-control",
                }
            ),

            "early_exit_minutes": forms.NumberInput(
                attrs={
                    "type": "number",
                    "min": "0",
                    "max": "180",
                    "class": "form-control",
                }
            ),
        }

class AttendanceForm(forms.ModelForm):

    class Meta:

        model = Attendance

        fields = [
            "employee",
            "date",
            "status",
            "check_in",
            "check_out",
            "remarks",
        ]

        widgets = {

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "check_in": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "check_out": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Enter remarks..."
                }
            ),
        }



class SalaryPayslipSettingsForm(forms.ModelForm):

    class Meta:

        model = SalaryPayslipSettings

        fields = [

            # Basic
            "payslip_title",
            "payslip_subtitle",
            "currency_symbol",

            # Numbering
            "payslip_prefix",
            "payslip_number_format",
            "auto_generate_number",

            # Company
            "show_company_name",
            "show_company_address",
            "show_company_phone",
            "show_company_email",
            "show_company_logo",

            # Employee
            "show_employee_id",
            "show_employee_department",
            "show_employee_designation",
            "show_joining_date",

            # Salary
            "show_basic_salary",
            "show_allowance",
            "show_deduction",
            "show_net_salary",

            # Attendance
            "show_working_days",
            "show_present_days",
            "show_absent_days",
            "show_leave_days",

            # Payment
            "show_payment_status",
            "show_payment_method",

            # Footer
            "footer_text",
            "show_signature",
            "authorized_person",
            "authorized_designation",

            # Print
            "paper_size",
            "orientation",
        ]

        widgets = {

            "payslip_title": forms.TextInput(
                attrs={
                    "placeholder": "Salary Payslip"
                }
            ),

            "payslip_subtitle": forms.TextInput(
                attrs={
                    "placeholder": "Employee Salary Statement"
                }
            ),

            "currency_symbol": forms.TextInput(
                attrs={
                    "placeholder": "₹"
                }
            ),

            "payslip_prefix": forms.TextInput(
                attrs={
                    "placeholder": "PAY"
                }
            ),

            "payslip_number_format": forms.TextInput(
                attrs={
                    "placeholder": "PAY-{year}-{number}"
                }
            ),

            "footer_text": forms.TextInput(
                attrs={
                    "placeholder": "This is a computer-generated payslip."
                }
            ),

            "authorized_person": forms.TextInput(
                attrs={
                    "placeholder": "Authorized Person"
                }
            ),

            "authorized_designation": forms.TextInput(
                attrs={
                    "placeholder": "HR Manager"
                }
            ),
        }


class SalaryTaxDeductionSettingsForm(forms.ModelForm):

    class Meta:

        model = SalaryTaxDeductionSettings

        fields = [

            # General
            "enable_deductions",
            "auto_apply_deductions",
            "calculation_basis",

            # PF
            "enable_pf",
            "pf_employee_percentage",

            # ESI
            "enable_esi",
            "esi_employee_percentage",

            # Professional Tax
            "enable_professional_tax",
            "professional_tax_amount",

            # Income Tax
            "enable_income_tax",
            "income_tax_percentage",

            # Loan
            "enable_loan_deduction",

            # Other
            "enable_other_deductions",

            # Salary protection
            "prevent_negative_salary",

            # Notifications
            "deduction_notifications",
            "tax_notifications",
        ]

        widgets = {

            "calculation_basis": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "pf_employee_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "max": "100",
                    "placeholder": "12.00"
                }
            ),

            "esi_employee_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "max": "100",
                    "placeholder": "0.00"
                }
            ),

            "professional_tax_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00"
                }
            ),

            "income_tax_percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "max": "100",
                    "placeholder": "0.00"
                }
            ),
        }


class SalaryBonusSettingsForm(forms.ModelForm):

    class Meta:

        model = SalaryBonusSettings

        fields = [
            "bonus_enabled",

            "default_bonus_type",
            "minimum_bonus_amount",
            "maximum_bonus_amount",

            "auto_include_in_payroll",
            "require_approval",
            "allow_manual_bonus",

            "taxable_bonus",
            "include_bonus_in_payslip",
            "include_bonus_in_salary",

            "notify_employee",
            "notify_admin",

            "performance_bonus_enabled",
            "festival_bonus_enabled",
            "annual_bonus_enabled",
            "referral_bonus_enabled",

            "default_description",
        ]

        widgets = {

            "minimum_bonus_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00"
                }
            ),

            "maximum_bonus_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00"
                }
            ),

            "default_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter default bonus description..."
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        minimum = cleaned_data.get(
            "minimum_bonus_amount"
        )

        maximum = cleaned_data.get(
            "maximum_bonus_amount"
        )

        if (
            minimum is not None
            and maximum is not None
            and maximum > 0
            and maximum < minimum
        ):
            self.add_error(
                "maximum_bonus_amount",
                "Maximum bonus amount cannot be less than minimum bonus amount."
            )

        return cleaned_data

class EmployeeSalarySettingsForm(forms.ModelForm):

    class Meta:

        model = EmployeeSalarySettings

        fields = [

            # General
            "salary_enabled",
            "default_currency",
            "salary_calculation_enabled",

            # Basic Salary
            "basic_salary_required",
            "allow_zero_salary",

            # Allowance
            "allowance_enabled",
            "default_allowance",

            # Deduction
            "deduction_enabled",
            "default_deduction",

            # Calculation
            "auto_calculate_net_salary",
            "include_attendance",
            "include_overtime",
            "include_bonus",
            "include_deductions",

            # Joining
            "salary_from_joining_date",
            "prorate_first_month_salary",

            # Payment
            "default_payment_method",

            # Notifications
            "salary_notifications",
            "salary_update_notifications",
            "salary_payment_notifications",

            # Employee Salary Management
            "allow_salary_edit",
            "allow_salary_history",
        ]

        widgets = {

            "default_currency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "₹",
                    "maxlength": "10",
                }
            ),

            "default_allowance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),

            "default_deduction": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),

            "default_payment_method": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "salary_enabled": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "salary_calculation_enabled": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "basic_salary_required": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "allow_zero_salary": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "allowance_enabled": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "deduction_enabled": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "auto_calculate_net_salary": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "include_attendance": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "include_overtime": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "include_bonus": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "include_deductions": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "salary_from_joining_date": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "prorate_first_month_salary": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "salary_notifications": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "salary_update_notifications": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "salary_payment_notifications": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "allow_salary_edit": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),

            "allow_salary_history": forms.CheckboxInput(
                attrs={
                    "class": "switch-input",
                }
            ),
        }

class SalaryNotificationSettingsForm(forms.ModelForm):

    class Meta:
        model = SalaryNotificationSettings

        fields = [
            # General
            "notifications_enabled",
            "email_notifications",
            "in_app_notifications",

            # Salary
            "salary_generated_notification",
            "salary_paid_notification",
            "salary_pending_notification",
            "salary_updated_notification",

            # Payroll
            "payroll_processed_notification",
            "payroll_failed_notification",
            "payroll_reminder_notification",

            # Employee
            "employee_salary_notification",
            "employee_payment_notification",

            # Reminder
            "salary_reminder_days",

            # Recipients
            "notify_admin",
            "notify_manager",
            "notify_employee",
        ]

        widgets = {

            "notifications_enabled": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "email_notifications": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "in_app_notifications": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "salary_generated_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "salary_paid_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "salary_pending_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "salary_updated_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "payroll_processed_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "payroll_failed_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "payroll_reminder_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "employee_salary_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "employee_payment_notification": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "notify_admin": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "notify_manager": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "notify_employee": forms.CheckboxInput(
                attrs={
                    "class": "notification-toggle"
                }
            ),

            "salary_reminder_days": forms.NumberInput(
                attrs={
                    "class": "number-input",
                    "min": "0",
                    "max": "30"
                }
            ),
        }

        labels = {
            "notifications_enabled": "Enable salary notifications",
            "email_notifications": "Email notifications",
            "in_app_notifications": "In-app notifications",

            "salary_generated_notification":
                "Salary generated",

            "salary_paid_notification":
                "Salary paid",

            "salary_pending_notification":
                "Salary pending",

            "salary_updated_notification":
                "Salary updated",

            "payroll_processed_notification":
                "Payroll processed",

            "payroll_failed_notification":
                "Payroll failed",

            "payroll_reminder_notification":
                "Payroll reminders",

            "employee_salary_notification":
                "Employee salary notifications",

            "employee_payment_notification":
                "Employee payment notifications",

            "salary_reminder_days":
                "Reminder days before salary date",

            "notify_admin":
                "Notify administrator",

            "notify_manager":
                "Notify manager",

            "notify_employee":
                "Notify employee",
        }

class SalaryThemeSettingsForm(forms.ModelForm):

    class Meta:

        model = SalaryThemeSettings

        fields = [
            "theme",
            "accent_color",
            "font_size",
            "dashboard_layout",
            "sidebar_style",
            "language",
            "time_zone",
            "show_breadcrumbs",
            "show_page_description",
            "compact_cards",
            "animations_enabled",
        ]

        widgets = {

            "theme": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "accent_color": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "accent-color-input"
                }
            ),

            "font_size": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "dashboard_layout": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "sidebar_style": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "language": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "time_zone": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "show_breadcrumbs": forms.CheckboxInput(
                attrs={
                    "class": "theme-checkbox"
                }
            ),

            "show_page_description": forms.CheckboxInput(
                attrs={
                    "class": "theme-checkbox"
                }
            ),

            "compact_cards": forms.CheckboxInput(
                attrs={
                    "class": "theme-checkbox"
                }
            ),

            "animations_enabled": forms.CheckboxInput(
                attrs={
                    "class": "theme-checkbox"
                }
            ),
        }