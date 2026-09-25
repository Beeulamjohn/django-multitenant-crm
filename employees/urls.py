from django.urls import path
from . import views

urlpatterns = [

    path(
        "employee_dashboard/",
        views.employee_dashboard,
        name="employee_dashboard"
    ),

    path(
        "list/",
        views.employee_list,
        name="employee_list"
    ),

    path(
        "employee_added/",
        views.employee_added,
        name="employee_added"
    ),

    path(
        "edit/<int:pk>/",
        views.edit_employee,
        name="edit_employee"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_employee,
        name="delete_employee"
    ),
    path("attendance/", views.employee_attendance_list, name="employee_attendance_list"),

    path("attendance/add/", views.employee_mark_attendance, name="employee_mark_attendance"),
     path(
        "employee_payroll/",
        views.employee_payroll,
        name="employee_payroll"
    ),

    path(
        "add_employee_payroll/",
        views.add_employee_payroll,
        name="add_employee_payroll"
    ),
    path("payroll/edit/<int:pk>/", views.edit_employee_payroll, name="edit_employee_payroll"),
    path("payroll/delete/<int:pk>/", views.delete_employee_payroll, name="delete_employee_payroll"),

    
    path(
        "departments/",
        views.department_list,
        name="department_list"
    ),

    path(
        "departments/add/",
        views.add_department,
        name="add_department"
    ),
    path(
        "departments/edit/<int:pk>/",
        views.edit_department,
        name="edit_department"
    ),

    path(
        "departments/delete/<int:pk>/",
        views.delete_department,
        name="delete_department"
    ),
     path(
        "employee_reports/",
        views.employee_reports,
        name="employee_reports",
    ),
    path(
        "employee_portal/",
        views.employee_portal,
        name="employee_portal"
    ),
    path(
    "employee-admin-login/",
    views.employee_admin_login,
    name="employee_admin_login",
),
    
    path(
        "employee-staff-login/",
        views.employee_staff_login,
        name="employee_staff_login"
    ),
   
    path(
        "settings/",
        views.employee_settings,
        name="employee_settings"
    ),

    path(
        "settings/general/",
        views.employee_general_settings,
        name="employee_general_settings"
    ),

    path(
        "settings/employee-profile/",
        views.employee_profile_settings,
        name="employee_profile_settings"
    ),


    path(
        "settings/departments-roles/",
        views.employee_departments_roles_settings,
        name="employee_departments_roles_settings"
    ),

    path(
        "settings/departments/<int:pk>/edit/",
        views.employee_department_edit,
        name="employee_department_edit"
    ),

    path(
        "settings/departments/<int:pk>/delete/",
        views.employee_department_delete,
        name="employee_department_delete"
    ),

    path(
        "settings/roles/<int:pk>/edit/",
        views.employee_role_edit,
        name="employee_role_edit"
    ),

    path(
        "settings/roles/<int:pk>/delete/",
        views.employee_role_delete,
        name="employee_role_delete"
    ),


    path(
        "settings/attendance/",
        views.employee_attendance_settings,
        name="employee_attendance_settings"
    ),

    path(
        "settings/leave/",
        views.employee_leave_settings,
        name="employee_leave_settings"
    ),

    path(
        "settings/payroll/",
        views.employee_payroll_settings,
        name="employee_payroll_settings"
    ),

    path(
        "settings/tax-statutory/",
        views.employee_tax_settings,
        name="employee_tax_settings"
    ),

    path(
        "settings/notifications/",
        views.employee_notification_settings,
        name="employee_notification_settings"
    ),

    path(
        "settings/documents/",
        views.employee_document_settings,
        name="employee_document_settings"
    ),

    path(
        "settings/reports/",
        views.employee_report_settings,
        name="employee_report_settings"
    ),

    path(
        "settings/security-permissions/",
        views.employee_security_settings,
        name="employee_security_settings"
    ),

    path(
        "settings/theme-appearance/",
        views.employee_theme_settings,
        name="employee_theme_settings"
    ),
   path(
        "logout/",
        views.logout_employee,
        name="employee_logout"
    ),

    
]