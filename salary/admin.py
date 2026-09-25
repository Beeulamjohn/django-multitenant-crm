from django.contrib import admin

from .models import (
    Salary,
    Employee,
    SalaryStructure,
    Payroll,
    Payslip,
    Bonus,
    Deduction,
    Attendance,
)

from .admin_site import salary_admin_site


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "name",
        "company",
        "department",
        "designation",
        "basic_salary",
        "status",
        "joined_date",
    )

    search_fields = (
        "employee_id",
        "name",
        "department",
        "designation",
        "company__company_name",
    )

    list_filter = (
        "company",
        "department",
        "status",
    )

    ordering = ("employee_id",)


class SalaryAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "company",
        "month",
        "year",
        "basic",
        "allowance",
        "deduction",
        "net_salary",
        "paid",
        "created_at",
    )

    search_fields = (
        "employee__name",
        "company__company_name",
    )

    list_filter = (
        "company",
        "month",
        "year",
        "paid",
    )

    ordering = (
        "-year",
        "-created_at",
    )


class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "company",
        "basic_salary",
        "hra",
        "allowance",
        "deduction",
        "net_salary",
    )

    search_fields = (
        "employee__name",
        "company__company_name",
    )

    list_filter = (
        "company",
    )


class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "company",
        "month",
        "year",
        "basic_salary",
        "allowance",
        "deduction",
        "net_salary",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "employee__name",
        "company__company_name",
    )

    list_filter = (
        "company",
        "payment_status",
        "month",
        "year",
    )

    ordering = (
        "-created_at",
    )


class PayslipAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "company",
        "month",
        "year",
        "net_salary",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "employee__name",
        "company__company_name",
    )

    list_filter = (
        "company",
        "payment_status",
    )

    ordering = (
        "-created_at",
    )


class BonusAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "company",
        "bonus_title",
        "bonus_type",
        "amount",
        "bonus_date",
        "payment_status",
    )

    search_fields = (
        "employee__name",
        "bonus_title",
        "company__company_name",
    )

    list_filter = (
        "company",
        "bonus_type",
        "payment_status",
    )

    ordering = (
        "-bonus_date",
    )


class DeductionAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "company",
        "deduction_title",
        "deduction_type",
        "amount",
        "deduction_date",
        "status",
    )

    search_fields = (
        "employee__name",
        "deduction_title",
        "company__company_name",
    )

    list_filter = (
        "company",
        "deduction_type",
        "status",
    )

    ordering = (
        "-deduction_date",
    )

class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "employee",
        "date",
        "status",
        "check_in",
        "check_out",
        "remarks",
    )

    search_fields = (
        "employee__name",
        "remarks",
    )

    list_filter = (
        "status",
        "date",
    )

    ordering = (
        "-date",
    )


salary_admin_site.register(Employee, EmployeeAdmin)
salary_admin_site.register(Salary, SalaryAdmin)
salary_admin_site.register(SalaryStructure, SalaryStructureAdmin)
salary_admin_site.register(Payroll, PayrollAdmin)
salary_admin_site.register(Payslip, PayslipAdmin)
salary_admin_site.register(Bonus, BonusAdmin)
salary_admin_site.register(Deduction, DeductionAdmin)
salary_admin_site.register(Attendance, AttendanceAdmin)