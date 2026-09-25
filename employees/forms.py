from django import forms
from .models import EmployeeDataSettings
from .models import EmployeeAttendanceSettings
from .models import EmployeeLeaveSettings
from .models import EmployeePayrollSettings
from .models import EmployeeTaxSettings
from .models import EmployeeNotificationSettings
from .models import EmployeeDocumentSettings
from .models import EmployeeReportSettings
from .models import EmployeeSecuritySettings
from .models import EmployeeThemeSettings
from .models import EmployeeCompanyProfile


from .models import (
    EmployeeDepartmentSettings,
    EmployeeRoleData,
)


class EmployeeDataSettingsForm(forms.ModelForm):

    class Meta:
        model = EmployeeDataSettings

        fields = [
            "employee_id_prefix",
            "employee_id_format",
            "auto_generate_employee_id",

            "default_employment_status",
            "default_department",
            "default_role",

            "attendance_tracking",
            "attendance_alerts",
            "late_arrival_tracking",
            "overtime_tracking",

            "payroll_enabled",
            "salary_currency",
            "salary_cycle",

            "employee_notifications",
            "attendance_notifications",
            "payroll_notifications",
            "leave_notifications",
        ]

        widgets = {

            "employee_id_prefix": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "EMP"
                }
            ),

            "employee_id_format": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "EMP-{year}-{number}"
                }
            ),

            "default_employment_status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "default_department": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Administration"
                }
            ),

            "default_role": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Staff"
                }
            ),

            "salary_currency": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "INR"
                }
            ),

            "salary_cycle": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }

class EmployeeCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeCompanyProfile
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

        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "company_type": forms.Select(attrs={"class": "form-control"}),
            "owner_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "pin_code": forms.TextInput(attrs={"class": "form-control"}),
            "gst_number": forms.TextInput(attrs={"class": "form-control"}),
            "pan_number": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
        }
class EmployeeDepartmentForm(forms.ModelForm):

    class Meta:
        model = EmployeeDepartmentSettings

        fields = [
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter department name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter department description",
                    "rows": 4,
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
        }


class EmployeeDepartmentForm(forms.ModelForm):

    class Meta:

        model = EmployeeDepartmentSettings

        fields = [
            "name",
            "description",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Human Resources",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter department description...",
                    "rows": 4,
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
        }


class EmployeeRoleForm(forms.ModelForm):

    class Meta:

        model = EmployeeRoleData

        fields = [
            "department",
            "name",
            "description",
            "is_active",
        ]

        widgets = {

            "department": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. HR Manager",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter role description...",
                    "rows": 4,
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
        }

class EmployeeAttendanceSettingsForm(forms.ModelForm):

    class Meta:
        model = EmployeeAttendanceSettings

        fields = [
            # Attendance
            "attendance_tracking",
            "attendance_method",
            "allow_employee_checkin",
            "allow_employee_checkout",

            # Working hours
            "work_start_time",
            "work_end_time",
            "late_after_minutes",
            "half_day_after_hours",
            "full_day_hours",

            # Weekly off
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",

            # Late / absence
            "late_arrival_tracking",
            "automatic_absent",
            "automatic_absent_after_minutes",

            # Overtime
            "overtime_tracking",
            "overtime_after_hours",

            # Notifications
            "attendance_alerts",
            "late_arrival_alerts",
            "absence_alerts",
            "employee_attendance_notifications",
        ]

        widgets = {

            "attendance_tracking": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "attendance_method": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "allow_employee_checkin": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "allow_employee_checkout": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "work_start_time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "work_end_time": forms.TimeInput(
                format="%H:%M",
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "late_after_minutes": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0"
                }
            ),

            "half_day_after_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.5"
                }
            ),

            "full_day_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.5"
                }
            ),

            "monday": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "tuesday": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "wednesday": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "thursday": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "friday": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "saturday": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "sunday": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "late_arrival_tracking": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "automatic_absent": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "automatic_absent_after_minutes": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0"
                }
            ),

            "overtime_tracking": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "overtime_after_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.5"
                }
            ),

            "attendance_alerts": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "late_arrival_alerts": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "absence_alerts": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),

            "employee_attendance_notifications": forms.CheckboxInput(
                attrs={"class": "setting-checkbox"}
            ),
        }


class EmployeeLeaveSettingsForm(forms.ModelForm):

    class Meta:
        model = EmployeeLeaveSettings

        fields = [
            # General
            "enable_leave_management",
            "leave_year_type",
            "allow_employee_leave_request",
            "require_leave_reason",
            "require_approval",

            # Leave balance
            "annual_leave_days",
            "sick_leave_days",
            "casual_leave_days",
            "unpaid_leave_allowed",
            "carry_forward_enabled",
            "carry_forward_days",

            # Accrual
            "leave_accrual",

            # Approval
            "manager_approval",
            "hr_approval",
            "admin_approval",

            # Notifications
            "employee_notifications",
            "manager_notifications",
            "hr_notifications",
            "leave_reminder_notifications",

            # Restrictions
            "minimum_notice_days",
            "maximum_consecutive_days",
            "allow_backdated_leave",
            "allow_half_day_leave",
        ]

        widgets = {

            "enable_leave_management": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "leave_year_type": forms.Select(
                attrs={
                    "class": "setting-select"
                }
            ),

            "allow_employee_leave_request": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "require_leave_reason": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "require_approval": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "annual_leave_days": forms.NumberInput(
                attrs={
                    "class": "setting-input",
                    "min": 0
                }
            ),

            "sick_leave_days": forms.NumberInput(
                attrs={
                    "class": "setting-input",
                    "min": 0
                }
            ),

            "casual_leave_days": forms.NumberInput(
                attrs={
                    "class": "setting-input",
                    "min": 0
                }
            ),

            "unpaid_leave_allowed": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "carry_forward_enabled": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "carry_forward_days": forms.NumberInput(
                attrs={
                    "class": "setting-input",
                    "min": 0
                }
            ),

            "leave_accrual": forms.Select(
                attrs={
                    "class": "setting-select"
                }
            ),

            "manager_approval": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "hr_approval": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "admin_approval": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "employee_notifications": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "manager_notifications": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "hr_notifications": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "leave_reminder_notifications": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "minimum_notice_days": forms.NumberInput(
                attrs={
                    "class": "setting-input",
                    "min": 0
                }
            ),

            "maximum_consecutive_days": forms.NumberInput(
                attrs={
                    "class": "setting-input",
                    "min": 1
                }
            ),

            "allow_backdated_leave": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),

            "allow_half_day_leave": forms.CheckboxInput(
                attrs={
                    "class": "setting-checkbox"
                }
            ),
        }

class EmployeePayrollSettingsForm(forms.ModelForm):

    class Meta:
        model = EmployeePayrollSettings

        fields = [
            # Payroll
            "payroll_enabled",
            "auto_calculate_salary",

            # Cycle
            "payroll_cycle",
            "payroll_day",

            # Currency
            "currency",
            "currency_symbol",

            # Salary components
            "include_basic_salary",
            "include_allowances",
            "include_bonus",
            "include_deductions",
            "include_overtime",

            # Attendance
            "attendance_based_salary",
            "unpaid_leave_deduction",
            "late_deduction",
            "overtime_enabled",

            # Tax
            "tax_deduction_enabled",
            "provident_fund_enabled",
            "professional_tax_enabled",

            # Payslip
            "payslip_enabled",
            "payslip_company_name",
            "payslip_employee_id",
            "payslip_department",
            "payslip_designation",
            "payslip_attendance",
            "payslip_salary_breakdown",

            # Notifications
            "payroll_notification",
            "payslip_notification",
            "payment_reminder",
        ]

        widgets = {

            "payroll_cycle": forms.Select(
                attrs={
                    "class": "settings-select"
                }
            ),

            "payroll_day": forms.NumberInput(
                attrs={
                    "class": "settings-input",
                    "min": "1",
                    "max": "31"
                }
            ),

            "currency": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "INR"
                }
            ),

            "currency_symbol": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "₹"
                }
            ),
        }

        labels = {
            "payroll_enabled": "Enable Payroll",
            "auto_calculate_salary": "Automatic Salary Calculation",

            "payroll_cycle": "Payroll Cycle",
            "payroll_day": "Payroll Processing Day",

            "currency": "Salary Currency",
            "currency_symbol": "Currency Symbol",

            "include_basic_salary": "Basic Salary",
            "include_allowances": "Allowances",
            "include_bonus": "Bonus",
            "include_deductions": "Deductions",
            "include_overtime": "Overtime",

            "attendance_based_salary": "Attendance Based Salary",
            "unpaid_leave_deduction": "Unpaid Leave Deduction",
            "late_deduction": "Late Arrival Deduction",
            "overtime_enabled": "Enable Overtime",

            "tax_deduction_enabled": "Tax Deduction",
            "provident_fund_enabled": "Provident Fund",
            "professional_tax_enabled": "Professional Tax",

            "payslip_enabled": "Enable Payslips",
            "payslip_company_name": "Company Name",
            "payslip_employee_id": "Employee ID",
            "payslip_department": "Department",
            "payslip_designation": "Designation",
            "payslip_attendance": "Attendance",
            "payslip_salary_breakdown": "Salary Breakdown",

            "payroll_notification": "Payroll Notification",
            "payslip_notification": "Payslip Notification",
            "payment_reminder": "Payment Reminder",
        }


class EmployeeTaxSettingsForm(forms.ModelForm):

    class Meta:
        model = EmployeeTaxSettings

        fields = [
            # General
            "enable_tax_settings",
            "tax_country",
            "financial_year",
            "currency",

            # PF
            "pf_enabled",
            "pf_employee_percentage",
            "pf_employer_percentage",
            "pf_account_number",

            # ESI
            "esi_enabled",
            "esi_employee_percentage",
            "esi_employer_percentage",
            "esi_number",

            # Professional Tax
            "professional_tax_enabled",
            "professional_tax_state",
            "professional_tax_number",

            # TDS
            "tds_enabled",
            "tan_number",
            "tds_deduction_method",

            # Other statutory
            "labour_welfare_enabled",
            "gratuity_enabled",
            "bonus_enabled",

            # Notifications
            "statutory_reminders",
            "compliance_notifications",
            "payroll_tax_notifications",
        ]

        widgets = {

            "tax_country": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "India"
                }
            ),

            "financial_year": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "2026-27"
                }
            ),

            "currency": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "INR"
                }
            ),

            "pf_employee_percentage": forms.NumberInput(
                attrs={
                    "class": "settings-input",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "pf_employer_percentage": forms.NumberInput(
                attrs={
                    "class": "settings-input",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "pf_account_number": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "PF Account Number"
                }
            ),

            "esi_employee_percentage": forms.NumberInput(
                attrs={
                    "class": "settings-input",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "esi_employer_percentage": forms.NumberInput(
                attrs={
                    "class": "settings-input",
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "esi_number": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "ESI Number"
                }
            ),

            "professional_tax_state": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "State"
                }
            ),

            "professional_tax_number": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "Professional Tax Number"
                }
            ),

            "tan_number": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "TAN Number"
                }
            ),

            "tds_deduction_method": forms.Select(
                attrs={
                    "class": "settings-select"
                }
            ),

            "enable_tax_settings": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "pf_enabled": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "esi_enabled": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "professional_tax_enabled": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "tds_enabled": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "labour_welfare_enabled": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "gratuity_enabled": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "bonus_enabled": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "statutory_reminders": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "compliance_notifications": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),

            "payroll_tax_notifications": forms.CheckboxInput(
                attrs={
                    "class": "settings-checkbox"
                }
            ),
        }


class EmployeeNotificationSettingsForm(
    forms.ModelForm
):

    class Meta:

        model = EmployeeNotificationSettings

        fields = [
            # General
            "employee_notifications",
            "admin_notifications",
            "manager_notifications",

            # Employee
            "new_employee_notification",
            "employee_profile_update_notification",
            "employee_status_change_notification",
            "employee_document_notification",

            # Attendance
            "attendance_notifications",
            "late_arrival_notifications",
            "absent_notifications",
            "overtime_notifications",

            # Leave
            "leave_notifications",
            "leave_request_notification",
            "leave_approval_notification",
            "leave_rejection_notification",

            # Payroll
            "payroll_notifications",
            "salary_generated_notification",
            "salary_paid_notification",
            "salary_pending_notification",

            # Documents
            "document_expiry_notification",
            "document_upload_notification",

            # Channels
            "email_notifications",
            "in_app_notifications",

            # Reminder
            "reminder_days",
        ]

        widgets = {

            "employee_notifications":
                forms.CheckboxInput(),

            "admin_notifications":
                forms.CheckboxInput(),

            "manager_notifications":
                forms.CheckboxInput(),

            "new_employee_notification":
                forms.CheckboxInput(),

            "employee_profile_update_notification":
                forms.CheckboxInput(),

            "employee_status_change_notification":
                forms.CheckboxInput(),

            "employee_document_notification":
                forms.CheckboxInput(),

            "attendance_notifications":
                forms.CheckboxInput(),

            "late_arrival_notifications":
                forms.CheckboxInput(),

            "absent_notifications":
                forms.CheckboxInput(),

            "overtime_notifications":
                forms.CheckboxInput(),

            "leave_notifications":
                forms.CheckboxInput(),

            "leave_request_notification":
                forms.CheckboxInput(),

            "leave_approval_notification":
                forms.CheckboxInput(),

            "leave_rejection_notification":
                forms.CheckboxInput(),

            "payroll_notifications":
                forms.CheckboxInput(),

            "salary_generated_notification":
                forms.CheckboxInput(),

            "salary_paid_notification":
                forms.CheckboxInput(),

            "salary_pending_notification":
                forms.CheckboxInput(),

            "document_expiry_notification":
                forms.CheckboxInput(),

            "document_upload_notification":
                forms.CheckboxInput(),

            "email_notifications":
                forms.CheckboxInput(),

            "in_app_notifications":
                forms.CheckboxInput(),

            "reminder_days":
                forms.NumberInput(
                    attrs={
                        "min": "0",
                        "max": "365",
                        "class": "notification-number-input"
                    }
                ),
        }

class EmployeeDocumentSettingsForm(forms.ModelForm):

    class Meta:

        model = EmployeeDocumentSettings

        fields = [
            # Document types
            "enable_identity_documents",
            "enable_address_documents",
            "enable_education_documents",
            "enable_experience_documents",
            "enable_bank_documents",
            "enable_contract_documents",
            "enable_other_documents",

            # Required documents
            "require_identity_document",
            "require_education_document",
            "require_experience_document",
            "require_bank_document",
            "require_contract_document",

            # Employee access
            "allow_employee_upload",
            "allow_employee_delete",
            "admin_approval_required",

            # File settings
            "max_file_size_mb",
            "allowed_file_types",

            # Notifications
            "notify_admin_on_upload",
            "notify_employee_on_approval",
            "notify_employee_on_rejection",
        ]

        widgets = {

            "max_file_size_mb": forms.NumberInput(
                attrs={
                    "class": "settings-input",
                    "min": "1",
                    "max": "100",
                }
            ),

            "allowed_file_types": forms.TextInput(
                attrs={
                    "class": "settings-input",
                    "placeholder": "PDF, JPG, JPEG, PNG",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # -----------------------------------------------------
        # CHECKBOX STYLING
        # -----------------------------------------------------

        checkbox_fields = [
            "enable_identity_documents",
            "enable_address_documents",
            "enable_education_documents",
            "enable_experience_documents",
            "enable_bank_documents",
            "enable_contract_documents",
            "enable_other_documents",

            "require_identity_document",
            "require_education_document",
            "require_experience_document",
            "require_bank_document",
            "require_contract_document",

            "allow_employee_upload",
            "allow_employee_delete",
            "admin_approval_required",

            "notify_admin_on_upload",
            "notify_employee_on_approval",
            "notify_employee_on_rejection",
        ]

        for field_name in checkbox_fields:

            self.fields[field_name].widget.attrs.update({
                "class": "settings-checkbox"
            })

        # -----------------------------------------------------
        # FILE TYPE VALIDATION
        # -----------------------------------------------------

        self.fields["allowed_file_types"].help_text = (
            "Example: PDF, JPG, JPEG, PNG"
        )

    def clean_max_file_size_mb(self):

        value = self.cleaned_data["max_file_size_mb"]

        if value < 1:
            raise forms.ValidationError(
                "File size must be at least 1 MB."
            )

        if value > 100:
            raise forms.ValidationError(
                "File size cannot exceed 100 MB."
            )

        return value



class EmployeeReportSettingsForm(forms.ModelForm):

    class Meta:

        model = EmployeeReportSettings

        fields = [
            # Report types
            "employee_report",
            "attendance_report",
            "leave_report",
            "payroll_report",
            "salary_report",
            "department_report",
            "employee_performance_report",
            "employee_document_report",

            # Dashboard
            "show_employee_summary",
            "show_department_summary",
            "show_attendance_summary",
            "show_leave_summary",
            "show_payroll_summary",

            # Access
            "allow_employee_reports",
            "allow_manager_reports",
            "allow_admin_reports",

            # Export
            "allow_pdf_export",
            "allow_excel_export",
            "allow_csv_export",

            # Period
            "default_report_period",
        ]

        widgets = {

            "employee_report": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "attendance_report": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "leave_report": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "payroll_report": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "salary_report": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "department_report": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "employee_performance_report": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "employee_document_report": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "show_employee_summary": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "show_department_summary": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "show_attendance_summary": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "show_leave_summary": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "show_payroll_summary": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "allow_employee_reports": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "allow_manager_reports": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "allow_admin_reports": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "allow_pdf_export": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "allow_excel_export": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "allow_csv_export": forms.CheckboxInput(
                attrs={"class": "report-toggle"}
            ),

            "default_report_period": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }


class EmployeeSecuritySettingsForm(forms.ModelForm):

    class Meta:

        model = EmployeeSecuritySettings

        fields = [
            # Login & Access
            "employee_login_enabled",
            "allow_employee_portal",
            "allow_employee_self_login",
            "require_login_for_employee_portal",

            # Password
            "password_min_length",
            "require_strong_password",
            "password_expiry_enabled",
            "password_expiry_days",

            # Session
            "session_timeout_enabled",
            "session_timeout_minutes",
            "allow_multiple_sessions",

            # Permissions
            "allow_profile_edit",
            "allow_attendance_view",
            "allow_leave_view",
            "allow_payroll_view",
            "allow_document_view",
            "allow_report_view",

            # Approval
            "require_admin_approval_for_profile_changes",
            "require_admin_approval_for_leave",
            "require_admin_approval_for_documents",

            # Notifications
            "notify_login",
            "notify_password_change",
            "notify_security_changes",

            # Audit
            "enable_security_audit_log",
        ]

        widgets = {

            # =====================================================
            # NUMBER INPUTS
            # =====================================================

            "password_min_length": forms.NumberInput(
                attrs={
                    "class": "security-number-input",
                    "min": "6",
                    "max": "128",
                }
            ),

            "password_expiry_days": forms.NumberInput(
                attrs={
                    "class": "security-number-input",
                    "min": "1",
                    "max": "3650",
                }
            ),

            "session_timeout_minutes": forms.NumberInput(
                attrs={
                    "class": "security-number-input",
                    "min": "5",
                    "max": "1440",
                }
            ),
        }

    def clean_password_min_length(self):

        value = self.cleaned_data["password_min_length"]

        if value < 6:
            raise forms.ValidationError(
                "Password minimum length must be at least 6 characters."
            )

        if value > 128:
            raise forms.ValidationError(
                "Password minimum length cannot exceed 128 characters."
            )

        return value

    def clean_password_expiry_days(self):

        value = self.cleaned_data["password_expiry_days"]

        if value < 1:
            raise forms.ValidationError(
                "Password expiry must be at least 1 day."
            )

        return value

    def clean_session_timeout_minutes(self):

        value = self.cleaned_data["session_timeout_minutes"]

        if value < 5:
            raise forms.ValidationError(
                "Session timeout must be at least 5 minutes."
            )

        return value


class EmployeeThemeSettingsForm(forms.ModelForm):

    class Meta:
        model = EmployeeThemeSettings

        fields = [
            "theme",
            "accent_color",
            "font_size",
            "sidebar_style",
            "dashboard_layout",
            "compact_mode",
            "reduced_motion",
            "show_breadcrumbs",
            "show_company_name",
        ]

        widgets = {

            "theme": forms.RadioSelect(
                attrs={
                    "class": "theme-radio"
                }
            ),

            "accent_color": forms.TextInput(
                attrs={
                    "type": "color",
                    "class": "color-picker"
                }
            ),

            "font_size": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "sidebar_style": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "dashboard_layout": forms.Select(
                attrs={
                    "class": "theme-select"
                }
            ),

            "compact_mode": forms.CheckboxInput(
                attrs={
                    "class": "settings-toggle"
                }
            ),

            "reduced_motion": forms.CheckboxInput(
                attrs={
                    "class": "settings-toggle"
                }
            ),

            "show_breadcrumbs": forms.CheckboxInput(
                attrs={
                    "class": "settings-toggle"
                }
            ),

            "show_company_name": forms.CheckboxInput(
                attrs={
                    "class": "settings-toggle"
                }
            ),
        }

    def clean_accent_color(self):

        color = self.cleaned_data.get("accent_color")

        if not color:
            return "#2563eb"

        if not color.startswith("#"):
            raise forms.ValidationError(
                "Accent color must start with #."
            )

        if len(color) != 7:
            raise forms.ValidationError(
                "Please select a valid color."
            )

        try:
            int(color[1:], 16)
        except ValueError:
            raise forms.ValidationError(
                "Please select a valid color."
            )

        return color