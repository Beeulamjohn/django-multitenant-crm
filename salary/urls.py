from django.urls import path
from . import views


urlpatterns = [

    path(
        "salary_dashboard",
        views.salary_dashboard,
        name="salary_dashboard"
    ),


    path(
        "employees/",
        views.employee_salary_list,
        name="employee_salary_list"
    ),

    path(
        "add-employee/",
        views.add_employee,
        name="add_employee"
    ),
    path(
        "employees/edit/<int:employee_id>/",
        views.salary_edit_employee,
        name="salary_edit_employee"
    ),

    # Delete Employee
    path(
        "employees/delete/<int:employee_id>/",
        views.salary_delete_employee,
        name="salary_delete_employee"
    ),






    path(
        "structures/",
        views.salary_structure_list,
        name="salary_structure_list"
    ),

path(
    "salary-structure/add/",
    views.add_salary_structure,
    name="add_salary_structure"
),

 path(
        "salary-structure/edit/<int:id>/",
        views.edit_salary_structure,
        name="edit_salary_structure"
    ),

    path(
        "salary-structure/delete/<int:id>/",
        views.delete_salary_structure,
        name="delete_salary_structure"
    ),




    path(
        "salary_payroll_list/",
        views.salary_payroll_list,
        name="salary_payroll_list"
    ),
    path(
        "salary_payroll_create/",
        views.salary_payroll_create,
        name="salary_payroll_create"
    ),

     path(
        "salary/payroll/edit/<int:id>/",
        views.salary_payroll_edit,
        name="salary_payroll_edit"
    ),


    # Delete Payroll
    path(
        "salary/payroll/delete/<int:id>/",
        views.salary_payroll_delete,
        name="salary_payroll_delete"
    ),



   path(
    "attendance/",
    views.attendance_dashboard,
    name="attendance_dashboard"
),

path(
    "attendance/mark/",
    views.mark_attendance,
    name="mark_attendance"
),

path(
    "attendance/edit/<int:id>/",
    views.edit_attendance,
    name="edit_attendance"
),

path(
    "attendance/delete/<int:id>/",
    views.delete_attendance,
    name="delete_attendance"
),



     path(
        "payslips/",
        views.payslip_list,
        name="payslip_list"
    ),



        path(
        "payslips/create/",
        views.payslip_create,
        name="payslip_create"
    ),


        path(
        "payslips/<int:pk>/edit/",
        views.payslip_edit,
        name="payslip_edit"
    ),

    path(
        "payslips/<int:pk>/delete/",
        views.payslip_delete,
        name="payslip_delete"
    ),


    
path(

    "bonus/",

    views.bonus_list,

    name="bonus_list"

),



path(

    "bonus/create/",

    views.bonus_create,

    name="bonus_create"

),



path(

    "bonus/delete/<int:id>/",

    views.bonus_delete,

    name="bonus_delete"

),






    path(
        "deductions/",
        views.deduction_list,
        name="deduction_list"
    ),
    path(

"deductions/create/",

views.deduction_create,

name="deduction_create"

),




path(

"deductions/delete/<int:id>/",

views.deduction_delete,

name="deduction_delete"

),

path(
    "salary/report/",
    views.salary_report,
    name="salary_report"
),
path(
    "salary/report/pdf/",
    views.salary_report_pdf,
    name="salary_report_pdf"
),
path(
        "salary-portal/",
        views.salary_portal,
        name="salary_portal",
    ),

    path(
        "salary-admin-login/",
        views.salary_admin_login,
        name="salary_admin_login",
    ),

    path(
        "salary-staff-login/",
        views.salary_staff_login,
        name="salary_staff_login",
    ),


path(
    "salary-settings/",
    views.salary_settings_page,
    name="salary_settings_page",
),

path(
    "salary-settings/payroll/",
    views.salary_payroll_settings,
    name="salary_payroll_settings",
),

path(
    "salary-settings/attendance/",
    views.salary_attendance_settings,
    name="salary_attendance_settings",
),

path(
    "salary-settings/payslip/",
    views.salary_payslip_settings,
    name="salary_payslip_settings",
),

path(
    "salary-settings/tax-deductions/",
    views.salary_tax_deductions_settings,
    name="salary_tax_deductions_settings",
),

path(
    "salary-settings/bonus/",
    views.salary_bonus_settings,
    name="salary_bonus_settings",
),

path(
    "salary-settings/employee-salary/",
    views.employee_salary_settings,
    name="employee_salary_settings",
),

path(
        "salary-settings/notifications/",
        views.salary_notification_settings,
        name="salary_notification_settings"
    ),

path(
    "salary-settings/theme/",
    views.salary_theme_settings,
    name="salary_theme_settings",
),
 path(
        "logout_salary/",
        views.logout_salary,
        name="logout_salary"
    ),


]