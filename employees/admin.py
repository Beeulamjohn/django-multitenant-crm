from django.contrib import admin
from .models import EmployeeCompanyProfile

from .models import (
    Employee,
    Attendance,
    Payroll,
    Staff,
    EmployeeDataSettings,
    EmployeeCompanyProfile,
    EmployeeDepartmentSettings,
    EmployeeRoleData,
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "first_name",
        "last_name",
        "company",
        "department",
        "role",
        "designation",
        "employment_status",
        "joining_date",
    )

    list_filter = (
        "employment_status",
        "company",
        "department",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "department",
        "role",
    )

    ordering = (
        "first_name",
        "last_name",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "company",
        "date",
        "status",
    )

    list_filter = (
        "status",
        "date",
        "company",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "employee__employee_id",
    )

    date_hierarchy = "date"

    ordering = (
        "-date",
    )



@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "company",
        "month",
        "year",
        "basic_salary",
        "bonus",
        "deduction",
        "net_salary",
        "payment_status",
    )

    list_filter = (
        "payment_status",
        "year",
        "month",
        "company",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "employee__employee_id",
    )

    ordering = (
        "-year",
        "-month",
    )


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = (
        "staff_id",
        "first_name",
        "last_name",
        "company",
        "designation",
        "salary",
        "joining_date",
        "status",
    )

    list_filter = (
        "status",
        "company",
        "designation",
    )

    search_fields = (
        "staff_id",
        "first_name",
        "last_name",
        "email",
        "phone",
    )


@admin.register(EmployeeDataSettings)
class EmployeeDataSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "employee_id_prefix",
        "employee_id_format",
        "auto_generate_employee_id",
        "default_employment_status",
        "attendance_tracking",
        "payroll_enabled",
        "salary_cycle",
    )

    list_filter = (
        "auto_generate_employee_id",
        "attendance_tracking",
        "payroll_enabled",
        "salary_cycle",
        "default_employment_status",
    )

    search_fields = (
        "company__company_name",
        "employee_id_prefix",
    )

@admin.register(EmployeeCompanyProfile)
class EmployeeCompanyProfileAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "company_name",
        "company_type",
        "owner_name",
        "email",
        "phone",
        "city",
        "state",
        "country",
        "updated_at",
    )

    list_filter = (
        "company_type",
        "state",
        "country",
    )

    search_fields = (
        "company__company_name",
        "company_name",
        "owner_name",
        "email",
        "phone",
        "gst_number",
        "pan_number",
        "city",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Company Information", {
            "fields": (
                "company",
                "company_name",
                "company_logo",
                "company_type",
                "owner_name",
                "email",
                "phone",
                "website",
            )
        }),
        ("Business Address", {
            "fields": (
                "address",
                "city",
                "state",
                "country",
                "pin_code",
            )
        }),
        ("Tax Information", {
            "fields": (
                "gst_number",
                "pan_number",
            )
        }),
        ("Description", {
            "fields": (
                "description",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

@admin.register(EmployeeDepartmentSettings)
class EmployeeDepartmentSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "company",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "company",
    )

    search_fields = (
        "name",
        "description",
        "company__company_name",
    )

    ordering = (
        "name",
    )


@admin.register(EmployeeRoleData)
class EmployeeRoleDataAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "department",
        "company",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "company",
        "department",
    )

    search_fields = (
        "name",
        "description",
        "department__name",
        "company__company_name",
    )

    ordering = (
        "department",
        "name",
    )